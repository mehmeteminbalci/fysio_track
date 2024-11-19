from guardian.shortcuts import get_objects_for_user

def user_has_patient_permission(user, permission, patient):
    """
    Kullanıcının belirli bir hasta üzerinde belirli bir izne sahip olup olmadığını kontrol eder.
    """
    return user.has_perm(permission, patient)

def get_user_patients(user):
    """
    Kullanıcının erişebileceği tüm hastaları döndürür.
    """
    return get_objects_for_user(user, 'patients.view_patient')
