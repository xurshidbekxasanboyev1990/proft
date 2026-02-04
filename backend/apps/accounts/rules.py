"""
Role-based permission rules using django-rules.
"""

import rules

# Predicates
@rules.predicate
def is_superadmin(user):
    """Check if user is a super admin."""
    return user.is_authenticated and user.role == 'superadmin'


@rules.predicate
def is_admin(user):
    """Check if user is an admin."""
    return user.is_authenticated and user.role == 'admin'


@rules.predicate
def is_teacher(user):
    """Check if user is a teacher."""
    return user.is_authenticated and user.role == 'teacher'


@rules.predicate
def is_admin_or_superadmin(user):
    """Check if user is admin or superadmin."""
    return user.is_authenticated and user.role in ['admin', 'superadmin']


@rules.predicate
def is_portfolio_owner(user, portfolio):
    """Check if user owns the portfolio."""
    if portfolio is None:
        return False
    return user.is_authenticated and portfolio.teacher_id == user.id


@rules.predicate
def can_view_portfolio(user, portfolio):
    """Check if user can view the portfolio."""
    if not user.is_authenticated:
        return False
    if user.role == 'superadmin':
        return True
    if user.role == 'admin':
        return True
    return portfolio.teacher_id == user.id


@rules.predicate
def can_edit_portfolio(user, portfolio):
    """Check if user can edit the portfolio."""
    if not user.is_authenticated:
        return False
    if user.role == 'superadmin':
        return True
    # Only owner can edit their own portfolio
    return portfolio.teacher_id == user.id


@rules.predicate
def can_delete_portfolio(user, portfolio):
    """Check if user can delete the portfolio."""
    if not user.is_authenticated:
        return False
    if user.role == 'superadmin':
        return True
    # Only owner can delete their own portfolio
    return portfolio.teacher_id == user.id


@rules.predicate
def can_approve_portfolio(user, portfolio):
    """Check if user can approve/reject the portfolio."""
    if not user.is_authenticated:
        return False
    return user.role in ['superadmin', 'admin']


# Permission rules for User model
rules.add_perm('accounts.view_user', is_superadmin)
rules.add_perm('accounts.add_user', is_superadmin)
rules.add_perm('accounts.change_user', is_superadmin)
rules.add_perm('accounts.delete_user', is_superadmin)

# Permission rules for Portfolio model
rules.add_perm('portfolios.view_portfolio', can_view_portfolio)
rules.add_perm('portfolios.add_portfolio', is_teacher | is_superadmin)
rules.add_perm('portfolios.change_portfolio', can_edit_portfolio)
rules.add_perm('portfolios.delete_portfolio', can_delete_portfolio)
rules.add_perm('portfolios.approve_portfolio', can_approve_portfolio)

# General permissions
rules.add_perm('accounts.manage_users', is_superadmin)
rules.add_perm('portfolios.manage_all_portfolios', is_superadmin)
rules.add_perm('portfolios.approve_reject', is_admin_or_superadmin)
