from rest_framework.routers import DefaultRouter
from .views import *

router_talles = DefaultRouter()
router_talles.register(r'talles', TallesViewSet)

router_tipus_producte = DefaultRouter()
router_tipus_producte.register(r'tipusproducte', TipusProducteViewSet)

router_productes = DefaultRouter()
router_productes.register(r'productes', ProducteViewSet)

router_productes_talles = DefaultRouter()
router_productes_talles.register(r'productestalles', ProducteTallesViewSet)

router_tipuspagament = DefaultRouter()
router_tipuspagament.register(r'tipuspagaments',TipusPagamentViewSet)

router_pagaments = DefaultRouter()
router_pagaments.register(r'pagaments', PagamentViewSet)

router_entrades = DefaultRouter()
router_entrades.register(r'entrades', EntradaViewSet)

router_detalls_pagament = DefaultRouter()
router_detalls_pagament.register(r'detallspagament', DetallsPagamentViewSet)

router_imatges_producte = DefaultRouter()
router_imatges_producte.register(r'imatgesproducte', ImatgesProducteViewSet)

router_enviaments= DefaultRouter()
router_imatges_producte.register(r'enviaments', EnviamentViewSet)


router_estatenviaments= DefaultRouter()
router_imatges_producte.register(r'estatenviaments', EstatEnviamentViewSet)