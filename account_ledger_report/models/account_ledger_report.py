from odoo import models, fields, api

class AccountLedgerReport(models.Model):
    _name = 'account.ledger.report'
    _description = 'Account Ledger Report'
    
    account_id = fields.Many2one('account.account', string="Account", required=True)

    date = fields.Date(string="Date")
    
    description = fields.Char(string="Description")
    
    debit = fields.Float(string="Debit")
    
    credit = fields.Float(string="Credit")
    
    balance = fields.Float(string="Balance")

    
    @api.model
    def get_ledger_data(self, account_id, start_date=None, end_date=None):
        """
        Fetches transactions for a given account including opening balance calculation, transactions and closing balance.
        """
        ledger_entries = []
        total_balance = 0

        account = self.env['account.account'].browse(account_id)
        
        if not account:
            return [] #if not account, return an empty list.

        domain = [('account_id', '=', account_id), ('move_id.state', '=', 'posted')]

        # Calculate Opening Balance (everything before start_date)
        if start_date:
            opening_balance_lines = self.env['account.move.line'].search(domain + [('date', '<', start_date)])
            opening_debit = sum(line.debit for line in opening_balance_lines)
            opening_credit = sum(line.credit for line in opening_balance_lines)
            opening_balance = opening_debit - opening_credit

            total_balance = opening_balance

            ledger_entries.append({
                'date': start_date,
                'description': 'Opening Balance',
                'debit': 0,
                'credit': 0,
                'balance': total_balance
            })

            # Now, we fetch transactions **from start_date onwards**
            domain += [('date', '>=', start_date)]

        if end_date:
            domain += [('date', '<=', end_date)]

        transactions = self.env['account.move.line'].search(domain, order='date asc')

        # Fetch Opening Balance
        # opening_move_line = self.env['account.move.line'].search([
        #     ('account_id', '=', account_id),
        #     ('move_id.state', '=', 'posted')
        # ], order='date asc', limit=1)

        # if opening_move_line:
        #     total_balance = opening_move_line.debit - opening_move_line.credit
        #     ledger_entries.append({
        #         'date': opening_move_line.date,
        #         'description': f"Opening Balance ({opening_move_line.move_id.name})",
        #         'debit': opening_move_line.debit,
        #         'credit': opening_move_line.credit,
        #         'balance': total_balance
        #     })
        
        # Fetch all transactions (except the opening balance)
        # transactions = self.env['account.move.line'].search([
        #     ('account_id', '=', account_id),
        #     ('move_id.state', '=', 'posted'), 
        #     ('id', '!=', opening_move_line.id)
        # ], order='date asc')

        for transaction in transactions:
            amount = transaction.debit - transaction.credit
            total_balance += amount
            ledger_entries.append({
                'date': transaction.date,
                'description': transaction.move_id.name or '',
                'debit': transaction.debit,
                'credit': transaction.credit,
                'balance': total_balance,

                # 'remaining_balance': total_balance
            })

        # Add Closing Balance Entry at the End
        if transactions:
            ledger_entries.append({
                'date': transactions[-1].date,  # Use the last transaction date
                'description': 'Closing Balance',
                'debit': 0,  # Closing balance has no debit
                'credit': 0,  # Closing balance has no credit
                'balance': total_balance  # Final computed balance
            })


        return ledger_entries

    def action_export_pdf(self):
        """
        Triggers the QWeb PDF report for customer ledger.
        """
        # return self.env.ref('customer_partner_ledger.customer_ledger_report').report_action(self)

        self.ensure_one()

        return self.env.ref('account_ledger_report.account_ledger_report').report_action(
            self.env['account.ledger.report'].create({'account_id': self.account_id.id})
            )
