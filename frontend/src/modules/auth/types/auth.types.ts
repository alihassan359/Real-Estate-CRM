/**
 * Auth Types - Authentication-related Types
 */


export interface AuthTypes {
  User: {
    id: string;
    email: string;
    firstName: string;
    lastName: string;
    role: 'admin' | 'manager' | 'operator';
  };
  LoginPayload: {
    email: string;
    password: string;
  };
  SignupPayload: {
    email: string;
    password: string;
    firstName: string;
    lastName: string;
  };
}

