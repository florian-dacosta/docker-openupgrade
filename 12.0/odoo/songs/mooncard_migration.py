from openupgradelib import openupgrade


def pre(ctx):
    openupgrade.update_module_names(ctx.env.cr, [('mooncard_invoice', 'base_newgen_payment_card')], merge_modules=True)
    openupgrade.rename_models(ctx.env.cr, [
        ('mooncard.transaction', 'newgen.payment.card.transaction'),
        ('mooncard.account.mapping', 'newgen.payment.card.account.mapping'),
        ('mooncard.card', 'newgen.payment.card'),
    ])
    openupgrade.rename_tables(ctx.env.cr, [
        ('mooncard_transaction', 'newgen_payment_card_transaction'),
        ('mooncard_account_mapping', 'newgen_payment.card_account_mapping'),
        ('mooncard_card', 'newgen_payment_card'),
    ]
    openupgrade.rename_fields(ctx.env, [
        ('newgen.payment.card.transaction', 'newgen_payment_card_transaction', 'merchant', 'vendor'),
    ])
    ctx.env.cr.execute("""
        UPDATE newgen_payment_card_transaction SET transaction_type = 'expense' WHERE transaction_type = 'presentment'
    """)

def post(ctx):
    # A bit hard to migrate fr_vat_20_amount and other 5.5, 2.1 and 10 fields to vat_rate
    # so we just delete all draft transaction, we will import it again
    ctx.env['newgen.payment.card.transaction'].search([('state', '=', 'draft')]).unlink()
