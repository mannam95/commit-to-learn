import React from 'react';
import { Button, ButtonProps } from '@mui/material';

export interface CustomButtonProps extends ButtonProps {
  label: string;
}

export const CustomButton: React.FC<CustomButtonProps> = ({ 
  label, 
  ...props 
}) => {
  return (
    <Button 
      variant="contained" 
      color="primary" 
      {...props}
    >
      {label}
    </Button>
  );
}; 