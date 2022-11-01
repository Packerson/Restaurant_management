# Restaurant_management
Inventory application for restaurants based on my previous professional expierence (7 years as a chef)

Aplication allows for creating user accounts with login access, creating product and supplier database, creating invoices, updating inventory based on invoice contents



## I use:
	django,
	psycopg2-binary,
	pytest,
	pytest-django,
	faker
	
## Links:

	main/				Main site
	register/			User register
	login/				Login user
	logout/				Logout user
	password/			User can change his password
	search/				Search products or company by name or NIP 
	invoice/			Invoices list
	invoice/{id}/			Information about invoice, update, delete
	invoice/add/			Add invoice
	invoive/update/{id}		Update invoice
	invoice/delete/{id}		delete invoice
	invoice/product/delete{id}	delete product from invoice
	company/			Company list
	company/{id}/ 			Information about company, update, delete
	company/add/			Add company
	company/delete/{id}		Delete company
	product/			List of products
	products/{id}			Information about product, update, delete
	product/add			Add product
	product/delete/{id}		Delete product
	inventory/			Inventory list, add product or invoice to inventory
	inventory/delete/{id}		Delete product from inventory
	

## Helpfull commands

	python manage.py add_products - add 150products
	python manage.py add_companys - add 150companys
