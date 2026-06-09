from User.models import User
import qrcode
from io import BytesIO
def check_permission(user_id, permission_name):
    print(user_id)
    print(permission_name)
    try:
        user = User.objects.get(pk=user_id)
        print(user)
    except User.DoesNotExist:
        return False

    # Get all roles for the user
    roles = user.rols.all()

    # Check if any of the roles have the specified permission
    for role in roles:
        print(role.permisos.filter(nom=permission_name))
        if role.permisos.filter(nom=permission_name).exists():
            return True

    return False

def generate_qr_code(data):
    # Crear el objeto QRCode
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    # Agregar los datos al QRCode
    qr.add_data(data)
    # Compilar el QRCode
    qr.make(fit=True)
    # Crear una imagen PIL
    img = qr.make_image(fill_color="black", back_color="white")
    # Guardar la imagen en un buffer de Bytes
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)
    # Retornar el buffer
    return buffer