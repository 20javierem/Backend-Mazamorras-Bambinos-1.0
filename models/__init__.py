from models.advance import Advance, AdvanceReadWithDetails, AdvanceRead, AdvanceBase
from models.day_sale import DaySale, DaySaleReadWithDetails, DaySaleRead, DaySaleReadCreate, DaySaleBase
from models.motion import Motion, MotionRead, MotionWithDetails, MotionBase
from models.place import Place, PlaceRead, PlaceReadWithType
from models.place_sale import PlaceSale, PlaceSaleReadWithDetails, PlaceSaleRead, \
    PlaceSaleBase, PlaceSaleCreateWithDetails, PlaceSaleReadCreateWithDetails, PlaceSaleReadForDaySale, \
    PlaceSaleReadForReport, PlaceSaleReadWithDaySale
from models.product import ProductRead, Product
from models.product_day_sale import ProductDaySale, ProductDaySaleRead, ProductDaySaleReadWithDetails, \
    ProductDaySaleReadCreate, ProductDaySaleReadReport
from models.product_place_sale import ProductPlaceSale, ProductPlaceSaleReadWithDetails, ProductPlaceSaleRead, \
    ProductPlaceSaleReadDaySaleCreate, ProductPlaceSaleCreate, ProductPlaceSaleReadReport
from models.transfer import TransferRead, Transfer, TransferBase
from models.type_place import TypePlace, TypePlaceRead
from models.type_worker import TypeWorker, TypeWorkerRead
from models.worker import Worker, WorkerReadWithType, WorkerRead

Place.update_forward_refs(TypePlace=TypePlace)

PlaceReadWithType.update_forward_refs(TypePlaceRead=TypePlaceRead)

Worker.update_forward_refs(TypeWorker=TypeWorker)

WorkerReadWithType.update_forward_refs(TypeWorkerRead=TypeWorkerRead)

Motion.update_forward_refs(DaySale=DaySale, PlaceSale=PlaceSale)

MotionWithDetails.update_forward_refs(DaySaleRead=DaySaleRead, PlaceSaleReadWithDaySale=PlaceSaleReadWithDaySale)

Advance.update_forward_refs(DaySale=DaySale, PlaceSale=PlaceSale, Worker=Worker)

AdvanceReadWithDetails.update_forward_refs(DaySaleRead=DaySaleRead,
                                           PlaceSaleReadWithDaySale=PlaceSaleReadWithDaySale,
                                           WorkerRead=WorkerRead)

Transfer.update_forward_refs(PlaceSale=PlaceSale, ProductDaySale=ProductDaySale)

PlaceSale.update_forward_refs(DaySale=DaySale, Worker=Worker, Place=Place, Advance=Advance,
                              Motion=Motion, Transfer=Transfer, ProductPlaceSale=ProductPlaceSale)

PlaceSaleReadWithDetails.update_forward_refs(WorkerRead=WorkerRead, PlaceRead=PlaceRead, DaySaleRead=DaySaleRead,
                                             AdvanceRead=AdvanceRead, MotionRead=MotionRead,
                                             TransferRead=TransferRead, ProductPlaceSale=ProductPlaceSale)

PlaceSaleCreateWithDetails.update_forward_refs(ProductPlaceSaleCreate=ProductPlaceSaleCreate, TransferBase=TransferBase,
                                               AdvanceBase=AdvanceBase, MotionBase=MotionBase)

DaySaleReadCreate.update_forward_refs(PlaceSaleReadCreateWithDetails=PlaceSaleReadCreateWithDetails,
                                      ProductDaySaleRead=ProductDaySaleRead)

DaySale.update_forward_refs(PlaceSale=PlaceSale, ProductDaySale=ProductDaySale, Advance=Advance, Motion=Motion)

DaySaleReadWithDetails.update_forward_refs(PlaceSaleReadForDaySale=PlaceSaleReadForDaySale,
                                           ProductDaySaleReadWithDetails=ProductDaySaleReadWithDetails,
                                           AdvanceRead=AdvanceRead,
                                           MotionRead=MotionRead)
PlaceSaleReadCreateWithDetails.update_forward_refs(ProductPlaceSaleReadDaySaleCreate=ProductPlaceSaleReadDaySaleCreate)

ProductDaySale.update_forward_refs(DaySale=DaySale, Product=Product, ProductPlaceSale=ProductPlaceSale)

ProductDaySaleReadWithDetails.update_forward_refs(ProductRead=ProductRead, ProductPlaceSaleRead=ProductPlaceSaleRead)

ProductDaySaleReadCreate.update_forward_refs(ProductPlaceSaleReadDaySaleCreate=ProductPlaceSaleReadDaySaleCreate)

ProductPlaceSale.update_forward_refs(ProductDaySale=ProductDaySale, PlaceSale=PlaceSale)

ProductPlaceSaleReadWithDetails.update_forward_refs(ProductDaySaleRead=ProductDaySaleRead, PlaceSaleRead=PlaceSaleRead)

PlaceSaleReadForDaySale.update_forward_refs(TransferRead=TransferRead, MotionRead=MotionRead, AdvanceRead=AdvanceRead)

PlaceSaleReadForReport.update_forward_refs(WorkerRead=WorkerRead, PlaceRead=PlaceRead, DaySaleRead=DaySaleRead)
PlaceSaleReadWithDaySale.update_forward_refs(DaySaleRead=DaySaleRead)

ProductDaySaleReadReport.update_forward_refs(DaySaleRead=DaySaleRead)

ProductPlaceSaleReadReport.update_forward_refs(PlaceSaleReadForReport=PlaceSaleReadForReport,
                                               ProductDaySaleReadReport=ProductDaySaleReadReport)
