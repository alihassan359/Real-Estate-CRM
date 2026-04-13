/**
 * Constants - Roles and Permissions
 */


export const ROLES = {
  ADMIN: 'admin',
  MANAGER: 'manager',
  OPERATOR: 'operator',
} as const;

export const PERMISSIONS = {
  // Deal permissions
  CREATE_DEAL: 'create_deal',
  EDIT_DEAL: 'edit_deal',
  DELETE_DEAL: 'delete_deal',
  VIEW_DEALS: 'view_deals',

  // Payment permissions
  VIEW_PAYMENTS: 'view_payments',
  CREATE_PAYMENT: 'create_payment',
  EDIT_PAYMENT: 'edit_payment',

  // User permissions
  MANAGE_USERS: 'manage_users',
  VIEW_USERS: 'view_users',

  // Admin permissions
  VIEW_REPORTS: 'view_reports',
  MANAGE_TENANTS: 'manage_tenants',
} as const;

export const ROLE_PERMISSIONS = {
  admin: [
    PERMISSIONS.CREATE_DEAL,
    PERMISSIONS.EDIT_DEAL,
    PERMISSIONS.DELETE_DEAL,
    PERMISSIONS.VIEW_DEALS,
    PERMISSIONS.VIEW_PAYMENTS,
    PERMISSIONS.CREATE_PAYMENT,
    PERMISSIONS.EDIT_PAYMENT,
    PERMISSIONS.MANAGE_USERS,
    PERMISSIONS.VIEW_USERS,
    PERMISSIONS.VIEW_REPORTS,
    PERMISSIONS.MANAGE_TENANTS,
  ],
  manager: [
    PERMISSIONS.CREATE_DEAL,
    PERMISSIONS.EDIT_DEAL,
    PERMISSIONS.VIEW_DEALS,
    PERMISSIONS.VIEW_PAYMENTS,
    PERMISSIONS.CREATE_PAYMENT,
    PERMISSIONS.VIEW_USERS,
  ],
  operator: [
    PERMISSIONS.CREATE_DEAL,
    PERMISSIONS.VIEW_DEALS,
    PERMISSIONS.VIEW_PAYMENTS,
  ],
} as const;

export const DEAL_STATUS = {
  ACTIVE: 'active',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled',
} as const;

export const PAYMENT_STATUS = {
  PENDING: 'pending',
  PAID: 'paid',
  OVERDUE: 'overdue',
  CANCELLED: 'cancelled',
} as const;

export const PAYMENT_METHODS = {
  BANK_TRANSFER: 'bank_transfer',
  CASH: 'cash',
  CHECK: 'check',
  ONLINE: 'online',
} as const;

