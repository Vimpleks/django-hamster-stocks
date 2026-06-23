from .index import index
from .threads import manufacturer, manufacturer_detail, thread_detail
from .stock import stock, manufacturers_stock, thread_stock_add, thread_stock_update, thread_stock_delete
from .basket import basket, manufacturers_basket, thread_basket_add, thread_basket_update, thread_basket_delete
from .project import projects, project_detail, add_project, edit_project, delete_project, manufacturers_project, \
    add_thread_project, update_thread_project, delete_thread_project
