"""
Custom OpenAPI schema customization hooks.
"""

from drf_spectacular.hooks import preprocess_schema_enums


def custom_preprocessing_hook(endpoints):
    """
    Custom preprocessing hook for API endpoints.
    Filter out internal or deprecated endpoints.
    """
    filtered = []
    for (path, path_regex, method, callback) in endpoints:
        # Skip internal endpoints
        if path.startswith('/api/internal/'):
            continue
        # Skip debug endpoints in production
        if path.startswith('/__debug__/'):
            continue
        filtered.append((path, path_regex, method, callback))
    return filtered


def custom_postprocessing_hook(result, generator, request, public):
    """
    Custom postprocessing hook for OpenAPI schema.
    Add custom metadata, organize tags, etc.
    """
    # Add custom x-logo for documentation
    result['info']['x-logo'] = {
        'url': '/static/logo.png',
        'altText': 'Portfolio Management System'
    }
    
    # Organize tags
    result['tags'] = [
        {
            'name': 'Authentication',
            'description': 'Hemis OAuth 2.0 autentifikatsiya va sessiya boshqaruvi',
        },
        {
            'name': 'Users',
            'description': 'Foydalanuvchilar va profillar boshqaruvi',
        },
        {
            'name': 'Portfolios',
            'description': 'Portfolio yaratish, tasdiqlash va boshqarish',
        },
        {
            'name': 'Categories',
            'description': 'Topshiriq kategoriyalari (Tezis, Esse, etc.)',
        },
        {
            'name': 'Assignments',
            'description': 'O\'qituvchilarga topshiriqlar berish va kuzatish',
        },
        {
            'name': 'Scoring',
            'description': 'Ball tizimi va baholash',
        },
        {
            'name': 'Analytics',
            'description': 'Dashboard, statistika va hisobotlar',
        },
        {
            'name': 'Reports',
            'description': 'Hisobot yaratish va eksport',
        },
    ]
    
    return result
