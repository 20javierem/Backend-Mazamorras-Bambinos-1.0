from models.advance import Advance, AdvanceReadWithDetails, AdvanceRead
from models.day_sale import DaySale, DaySaleReadWithDetails, DaySaleRead
from models.expense import Expense, ExpenseRead, ExpenseWithDetails
from models.place import Place, PlaceRead, PlaceReadWithType
from models.place_sale import PlaceSale, PlaceSaleReadWithDetails, PlaceSaleRead
from models.product import ProductRead, Product
from models.product_day_sale import ProductDaySale, ProductDaySaleRead, ProductDaySaleReadWithDetails
from models.product_place_sale import ProductPlaceSale, ProductPlaceSaleReadWithDetails, ProductPlaceSaleRead
from models.transfer import TransferRead, Transfer
from models.type_place import TypePlace, TypePlaceRead
from models.type_worker import TypeWorker, TypeWorkerRead
from models.worker import Worker, WorkerReadWithType, WorkerRead

Advance.update_forward_refs(DaySale=DaySale,
                            PlaceSale=PlaceSale,
                            Worker=Worker)
AdvanceReadWithDetails.update_forward_refs(DaySaleRead=DaySaleRead,
                                           PlaceSaleRead=PlaceSaleRead,
                                           WorkerRead=WorkerRead)
DaySale.update_forward_refs(PlaceSale=PlaceSale,
                            ProductDaySale=ProductDaySale,
                            Advance=Advance, Expense=Expense)
DaySaleReadWithDetails.update_forward_refs(PlaceSaleRead=PlaceSaleRead,
                                           ProductDaySaleRead=ProductDaySaleRead,
                                           AdvanceRead=AdvanceRead,
                                           Expense=Expense)
Expense.update_forward_refs(DaySale=DaySale,
                            PlaceSale=PlaceSale)
ExpenseWithDetails.update_forward_refs(DaySaleRead=DaySaleRead,
                                       PlaceSaleRead=PlaceSaleRead)
Place.update_forward_refs(TypePlace=TypePlace)
PlaceReadWithType.update_forward_refs(TypePlaceRead=TypePlaceRead)
PlaceSale.update_forward_refs(Worker=Worker,
                              Place=Place,
                              DaySale=DaySale,
                              Advance=Advance,
                              Expense=Expense,
                              Transfer=Transfer,
                              ProductPlaceSale=ProductPlaceSale)
PlaceSaleReadWithDetails.update_forward_refs(WorkerRead=WorkerRead,
                                             PlaceRead=PlaceRead,
                                             DaySaleRead=DaySaleRead,
                                             AdvanceRead=AdvanceRead,
                                             ExpenseRead=ExpenseRead,
                                             TransferRead=TransferRead,
                                             ProductPlaceSale=ProductPlaceSale)
ProductDaySale.update_forward_refs(DaySale=DaySale,
                                   Product=Product,
                                   ProductPlaceSale=ProductPlaceSale)
ProductDaySaleReadWithDetails.update_forward_refs(ProductRead=ProductRead,
                                                  ProductPlaceSaleRead=ProductPlaceSaleRead)
ProductPlaceSale.update_forward_refs(ProductDaySale=ProductDaySale,
                                     PlaceSale=PlaceSale)
ProductPlaceSaleReadWithDetails.update_forward_refs(ProductDaySaleRead=ProductDaySaleRead,
                                                    PlaceSaleRead=PlaceSaleRead)
Transfer.update_forward_refs(PlaceSale=PlaceSale,
                             Product=Product)
Worker.update_forward_refs(TypeWorker=TypeWorker)
WorkerReadWithType.update_forward_refs(TypeWorkerRead=TypeWorkerRead)