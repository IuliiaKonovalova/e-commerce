"""Urls for the personnel app."""
from django.urls import path
from .views import (
    ProductsTableView,
    ProductFullDetailView,
    AddProductView,
    EditProductView,
    DeleteProductView,
    AddImageToProductAJAXView,
    EditImageToProductAJAXView,
    DeleteImageToProductAJAXView,
    ProductInventoryDetailsView,
    AddProductInventoryDetailsView,
    GetTypeAttributeAJAXView,
    ProductInventoryCreateAJAXView,
    EditProductInventoryView,
    UpdateProductInventoryAJAXView,
    DeleteProductInventoryView,
    ProductInventoriesTableView,
    CategoriesTableView,
    AddCategoryView,
    EditCategoryView,
    DeleteCategoryView,
    BrandsTableView,
    BrandDetailView,
    AddBrandView,
    EditBrandView,
    DeleteBrandView,
    TagsTableView,
    TagDetailView,
    AddTagView,
    EditTagView,
    DeleteTagView,
    StockView,
    AddStockView,
    UpdateStockView,
    DeleteStockView,
    ProductTypesListView,
    AddProductTypeView,
    UpdateProductTypeView,
    DeleteProductTypeView,
    AttributesListView,
    AddAttributeView,
    EditAttributeView,
    DeleteAttributeView,
)


urlpatterns = [
    path(
        'products_table/',
        ProductsTableView.as_view(),
        name='products_table'
    ),
    path(
        'product/<int:pk>/',
        ProductFullDetailView.as_view(),
        name='product_detail_full'
    ),
    path(
        'product/add/',
        AddProductView.as_view(),
        name='add_product'
    ),
    path(
        'product/<int:pk>/edit/',
        EditProductView.as_view(),
        name='edit_product'
    ),
    path(
        'product/<int:pk>/delete/',
        DeleteProductView.as_view(),
        name='delete_product'
    ),
    path(
        'add_product_image/',
        AddImageToProductAJAXView.as_view(),
        name='add_product_image'
    ),
    path(
        'edit_product_image/',
        EditImageToProductAJAXView.as_view(),
        name='edit_product_image'
    ),
    path(
        'delete_product_image/',
        DeleteImageToProductAJAXView.as_view(),
        name='delete_product_image'
    ),
    path(
        'product/<int:pk>/inventory/<int:inventory_pk>/',
        ProductInventoryDetailsView.as_view(),
        name='product_inventory_details'
    ),
    path(
        'product/<int:pk>/add_inventory/',
        AddProductInventoryDetailsView.as_view(),
        name='add_product_inventory_details'
    ),
    path(
        'get_type_attribute/',
        GetTypeAttributeAJAXView.as_view(),
        name='get_type_attribute'
    ),
    path(
        'product_inventory_create/',
        ProductInventoryCreateAJAXView.as_view(),
        name='product_inventory_create'
    ),
    path(
        'product/<int:pk>/edit_inventory/<int:inventory_pk>/',
        EditProductInventoryView.as_view(),
        name='edit_product_inventory'
    ),
    path(
        'product_inventory_update/',
        UpdateProductInventoryAJAXView.as_view(),
        name='product_inventory_update'
    ),
    path(
        'product/<int:pk>/delete_inventory/<int:inventory_pk>/',
        DeleteProductInventoryView.as_view(),
        name='delete_product_inventory'
    ),
    path(
        'product_inventories_table/',
        ProductInventoriesTableView.as_view(),
        name='product_inventories_table'
    ),
    path(
        'categories_table/',
        CategoriesTableView.as_view(),
        name='categories_table'
    ),
    path(
        'category/add/',
        AddCategoryView.as_view(),
        name='add_category'
    ),
    path(
        'category/<int:category_pk>/edit/',
        EditCategoryView.as_view(),
        name='edit_category'
    ),
    path(
        'category/<int:category_pk>/delete/',
        DeleteCategoryView.as_view(),
        name='delete_category'
    ),
    path(
        'brands_table/',
        BrandsTableView.as_view(),
        name='brands_table'
    ),
    path(
        'brand/<int:brand_pk>/',
        BrandDetailView.as_view(),
        name='brand_detail'
    ),
    path(
        'brand/add/',
        AddBrandView.as_view(),
        name='add_brand'
    ),
    path(
        'brand/<int:brand_pk>/edit/',
        EditBrandView.as_view(),
        name='edit_brand'
    ),
    path(
        'brand/<int:brand_pk>/delete/',
        DeleteBrandView.as_view(),
        name='delete_brand'
    ),
    path(
        'tags_table/',
        TagsTableView.as_view(),
        name='tags_table'
    ),
    path(
        'tag/<int:tag_pk>/',
        TagDetailView.as_view(),
        name='tag_detail'
    ),
    path(
        'tag/add/',
        AddTagView.as_view(),
        name='add_tag'
    ),
    path(
        'tag/<int:tag_pk>/edit/',
        EditTagView.as_view(),
        name='edit_tag'
    ),
    path(
        'tag/<int:tag_pk>/delete/',
        DeleteTagView.as_view(),
        name='delete_tag'
    ),
    path(
        'stock/',
        StockView.as_view(),
        name='stock'
    ),
    path(
        'product/<int:pk>/inventory/<int:inventory_pk>/add_stock/',
        AddStockView.as_view(),
        name='add_stock'
    ),
    path(
        (
            'product/<int:pk>/inventory/<int:inventory_pk>/' +
            'update_stock/<int:stock_pk>/'
        ),
        UpdateStockView.as_view(),
        name='update_stock'
    ),
    path(
        (
            'product/<int:pk>/inventory/<int:inventory_pk>/' +
            'delete_stock/<int:stock_pk>/'
        ),
        DeleteStockView.as_view(),
        name='delete_stock'
    ),
    path(
        'product_types_table/',
        ProductTypesListView.as_view(),
        name='product_types_table'
    ),
    path(
        'product_type/add/',
        AddProductTypeView.as_view(),
        name='add_product_type'
    ),
    path(
        'product_type/<int:pk>/edit/',
        UpdateProductTypeView.as_view(),
        name='edit_product_type'
    ),
    path(
        'product_type/<int:pk>/delete/',
        DeleteProductTypeView.as_view(),
        name='delete_product_type'
    ),
    path(
        'attributes/',
        AttributesListView.as_view(),
        name='product_type_attributes'
    ),
    path(
        'attribute/add/',
        AddAttributeView.as_view(),
        name='add_attribute'
    ),
    path(
        'attribute/<int:pk>/edit/',
        EditAttributeView.as_view(),
        name='edit_attribute'
    ),
    path(
        'attribute/<int:pk>/delete/',
        DeleteAttributeView.as_view(),
        name='delete_attribute'
    ),
]
