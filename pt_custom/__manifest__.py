{
    'name': "App Z",
    'version': '17.0.0.1.0',
    'depends': ['base', 'sale_management', 'account_accountant', 'mail', 'purchase', 'stock', 'report_xlsx'
                ],
    'author': "hosny",
    'category': '',
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        # 'data/sale_order_view.xml',
        'data/email_view.xml',
        'data/ir_corn.xml',
        # 'data/stock_view.xml',
        'views/base_menu.xml',
        'views/property_one_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
        'views/sale_order_view.xml',
        'views/building_view.xml',
        'views/stock_view.xml',
        # 'views/email_view.xml',
        'views/property_history_view.xml',
        'wizard/change_state_wizard_view.xml',
        'wizard/change_area_wizard_view.xml',
        'reports/property_report.xml',
    ],
    'assets': {
        'web.assets_backend': ['pt_custom/static/src/property.css']
    },
    'application': True,
}
