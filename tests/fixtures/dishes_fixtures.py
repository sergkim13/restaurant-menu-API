import uuid

fake_id = uuid.uuid4()
new_dish = {'title': 'Borsh', 'description': 'best borsh', 'price': 300}
upd_dish = {
    'title': 'Updated borsh',
    'description': 'brand new borsh', 'price': 450,
}
dish_not_found = {'detail': 'dish not found'}
dish_deleted = {'status': True, 'message': 'The dish has been deleted'}
