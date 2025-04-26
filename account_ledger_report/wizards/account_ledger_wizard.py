from odoo import models, fields, api

class AccountLedgerWizard(models.TransientModel):
    _name = 'account.ledger.wizard'
    _description = 'Account Ledger Wizard'

    account_id = fields.Many2one('account.account', string="Account", required=True)

    def action_generate_account_ledger(self):
        """
        Triggers the QWeb PDF report for the account ledger.
        """
        self.ensure_one()

        return self.env.ref('account_ledger_report.account_ledger_report').report_action(
            self.env['account.ledger.report'].create({'account_id': self.account_id.id})
        )

    def action_preview_account_report(self):
        self.ensure_one()

        # Clear previous records for this account (Optional)
        self.env['account.ledger.report'].search([('account_id', '=', self.account_id.id)]).unlink()

        # Get ledger data
        ledger_data = self.env['account.ledger.report'].get_ledger_data(self.account_id.id)

        # Create records
        for entry in ledger_data:
            self.env['account.ledger.report'].create({
                'account_id': self.account_id.id,
                'date': entry.get('date'),
                'description': entry.get('description'),
                'debit': entry.get('debit'),
                'credit': entry.get('credit'),
                'balance': entry.get('balance'),
            })

        # Return an action to open the tree view
        return {
            'type': 'ir.actions.act_window',
            'name': 'Account Ledger',
            'view_mode': 'tree',
            'res_model': 'account.ledger.report',
            'views': [(self.env.ref('account_ledger_report.view_account_ledger_report_tree').id, 'tree')],
            'domain': [('account_id', '=', self.account_id.id)],
            'target': 'current',
        }

