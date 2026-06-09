import django
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TimeOut.settings')
django.setup()

from django.core.management import call_command

from Botiga.models import (DetallsPagament, Entrada, Enviament, Pagament,
                            ImatgesProducte, ProducteTalles, Producte,
                            TipusProducte, Talles, TipusPagament, EstatEnviament)
from noticies.models import noticies as Noticia
from Esdeveniment.models import Esdeveniment, TipusEsdeveniment
from Equip.models import EquipUsuaris, Equip, Esport, Categoria, Divisio
from Patrocinadors.models import Patrocinador
from User.models import RolUsuari, User, Rol, Permisos

print("=" * 50)
print("SEED DATA - Sabadell Rugby Club")
print("=" * 50)

# ── 1. NETEJA (ordre invers de FK) ──────────────────
print("\n[1/3] Netejant dades existents...")

DetallsPagament.objects.all().delete()
print("  ✓ DetallsPagament")

Entrada.objects.all().delete()
print("  ✓ Entrada")

Enviament.objects.all().delete()
print("  ✓ Enviament")

Pagament.objects.all().delete()
print("  ✓ Pagament")

ImatgesProducte.objects.all().delete()
print("  ✓ ImatgesProducte")

ProducteTalles.objects.all().delete()
print("  ✓ ProducteTalles")

Producte.objects.all().delete()
print("  ✓ Producte")

TipusProducte.objects.all().delete()
print("  ✓ TipusProducte")

Talles.objects.all().delete()
print("  ✓ Talles")

TipusPagament.objects.all().delete()
print("  ✓ TipusPagament")

EstatEnviament.objects.all().delete()
print("  ✓ EstatEnviament")

Noticia.objects.all().delete()
print("  ✓ Noticies")

Esdeveniment.objects.all().delete()
print("  ✓ Esdeveniments")

TipusEsdeveniment.objects.all().delete()
print("  ✓ TipusEsdeveniment")

EquipUsuaris.objects.all().delete()
print("  ✓ EquipUsuaris")

Equip.objects.all().delete()
print("  ✓ Equip")

Esport.objects.all().delete()
Categoria.objects.all().delete()
Divisio.objects.all().delete()
print("  ✓ Esport / Categoria / Divisio")

Patrocinador.objects.all().delete()
print("  ✓ Patrocinadors")

RolUsuari.objects.all().delete()
print("  ✓ RolUsuari")

# Esborrem tots els usuaris EXCEPTE l'admin
deleted_users = User.objects.exclude(username='admin').count()
User.objects.exclude(username='admin').delete()
print(f"  ✓ Users ({deleted_users} esborrats, 'admin' conservat)")

Rol.objects.all().delete()
print("  ✓ Rols (i relacions rol-permisos)")

Permisos.objects.all().delete()
print("  ✓ Permisos")

# ── 2. CÀRREGA DE FIXTURES ──────────────────────────
print("\n[2/3] Carregant fixtures...")

fixtures_ordre = [
    # User
    ("permisos_data",          "Permisos (25)"),
    ("rol_data",               "Rols (7)"),
    ("rolpermisos_data",       "Rol-Permisos (58)"),
    ("users_data",             "Users (60)"),
    ("rolusuari_data",         "RolUsuari (37)"),
    # Equip
    ("esport_data",            "Esports (1)"),
    ("categoria_data",         "Categories (8)"),
    ("divisio_data",           "Divisions (2)"),
    ("equips_data",            "Equips (3)"),
    ("equipsUsuaris_data",     "EquipUsuaris (26)"),
    # Esdeveniment
    ("tipusesdeveniments_data","TipusEsdeveniment (5)"),
    ("esdeveniments_data",     "Esdeveniments (15, dates 2030-2031)"),
    # Noticies
    ("noticies_data",          "Noticies (6)"),
    # Patrocinadors
    ("patrocinadors_data",     "Patrocinadors (8)"),
    # Botiga
    ("tipusproducte_data",     "TipusProducte (7)"),
    ("talles_data",            "Talles (7)"),
    ("productes_data",         "Productes (11)"),
    ("productestalles_data",   "ProducteTalles (48)"),
    ("tipuspagament_data",     "TipusPagament (3)"),
    ("estatenviament_data",    "EstatEnviament (3)"),
    ("imatgesproducte_data",   "ImatgesProducte (30)"),
    ("pagaments_data",         "Pagaments (20)"),
    ("detallspagament_data",   "DetallsPagament (12)"),
    ("entrades_data",          "Entrades (10)"),
    ("enviaments_data",        "Enviaments (8)"),
]

errors = []
for fixture_name, description in fixtures_ordre:
    try:
        call_command('loaddata', fixture_name, verbosity=0)
        print(f"  ✓ {description}")
    except Exception as e:
        print(f"  ✗ ERROR a {fixture_name}: {e}", file=sys.stderr)
        errors.append(fixture_name)

# ── 3. RESUM ────────────────────────────────────────
print("\n[3/3] Resum final")
print(f"  Users:         {User.objects.count()}")
print(f"  Rols:          {Rol.objects.count()}")
print(f"  Permisos:      {Permisos.objects.count()}")
print(f"  Equips:        {Equip.objects.count()}")
print(f"  Esdeveniments: {Esdeveniment.objects.count()}")
print(f"  Noticies:      {Noticia.objects.count()}")
print(f"  Patrocinadors: {Patrocinador.objects.count()}")
print(f"  Productes:     {Producte.objects.count()}")
print(f"  ImatgesProducte: {ImatgesProducte.objects.count()}")

from Botiga.models import Pagament, DetallsPagament, Entrada, Enviament
print(f"  Pagaments:       {Pagament.objects.count()}")
print(f"  DetallsPagament: {DetallsPagament.objects.count()}")
print(f"  Entrades:        {Entrada.objects.count()}")
print(f"  Enviaments:      {Enviament.objects.count()}")

# ── 4. ASSIGNAR ROL ADMINISTRADOR A L'USUARI ADMIN ──
print("\n[4/4] Assignant rol Administrador/a a l'usuari 'admin'...")
try:
    admin_user = User.objects.get(username='admin')
    rol_admin = Rol.objects.get(nom='Administrador/a')
    RolUsuari.objects.get_or_create(user=admin_user, rol=rol_admin)
    print("  ✓ admin → Administrador/a")
except User.DoesNotExist:
    print("  ⚠ Usuari 'admin' no trobat (executa create_superuser.py primer)", file=sys.stderr)
except Rol.DoesNotExist:
    print("  ⚠ Rol 'Administrador/a' no trobat", file=sys.stderr)

if errors:
    print(f"\n⚠ Fixtures amb errors: {', '.join(errors)}", file=sys.stderr)
    sys.exit(1)
else:
    print("\n✓ Seed completat correctament!")
    print("  Usuari admin: admin / admin (tots els permisos)")
