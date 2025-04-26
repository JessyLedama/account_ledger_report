from odoo import models, api

class ResAccount(models.Model):
    _inherit = "account.account"

    def action_open_account_ledger(self):
        """
        Opens the ledger report when the action is selected.
        """
        return self.env.ref('account_ledger_report.account_ledger_report').report_action(self)
