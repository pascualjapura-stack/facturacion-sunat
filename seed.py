"""
Ejecutar una sola vez para crear la empresa y el usuario administrador inicial:
    python seed.py
"""
from app.database import SessionLocal, Base, engine
from app import models, schemas, crud, auth

Base.metadata.create_all(bind=engine)
db = SessionLocal()

RUC_DEMO = "20123456789"
existente = db.query(models.Empresa).filter(models.Empresa.ruc == RUC_DEMO).first()

if existente:
    print(f"La empresa demo ya existe (id={existente.id}). No se creó nada nuevo.")
else:
    empresa = crud.crear_empresa(db, schemas.EmpresaCreate(
        ruc=RUC_DEMO,
        razon_social="MI EMPRESA DEMO S.A.C.",
        nombre_comercial="Mi Empresa Demo",
        direccion_fiscal="Av. Ejemplo 123, Lima",
        ubigeo="150101",
        # Completa estos datos con tu proveedor OSE real (Nubefact, Efact, etc.)
        ose_token="COMPLETAR_CON_TU_TOKEN_OSE",
        ose_ruc_proveedor=RUC_DEMO,
    ))

    admin = models.Usuario(
        empresa_id=empresa.id,
        nombre="Administrador",
        email="admin@miempresa.com",
        password_hash=auth.hash_password("admin123"),
        rol="admin",
    )
    db.add(admin)
    db.commit()

    print("Empresa y usuario admin creados:")
    print(f"  Empresa: {empresa.razon_social} (RUC {empresa.ruc})")
    print("  Login:   admin@miempresa.com / admin123")
    print("  ⚠️  Cambia la contraseña y configura tu ose_token real antes de producción.")

db.close()
