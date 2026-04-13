/**
 * Form Input Component - Reusable Form Field
 */


'use client';

import React from 'react';

interface FormInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  helperText?: string;
}

export const FormInput: React.FC<FormInputProps> = ({
  label,
  error,
  helperText,
  className,
  ...props
}) => {
  return (
    <div className="w-full">
      <label className="block text-sm font-medium text-gray-700 mb-2">{label}</label>
      <input
        className={`input-base ${error ? 'border-red-500 focus:ring-red-500' : ''} ${className}`}
        {...props}
      />
      {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
      {helperText && <p className="mt-1 text-sm text-gray-500">{helperText}</p>}
    </div>
  );
};

