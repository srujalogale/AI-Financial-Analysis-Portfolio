import * as React from "react";

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
}

export function Button({
  children,
  className = "",
  ...props
}: ButtonProps) {
  return (
    <button
      className={`rounded-md bg-black px-4 py-2 text-white hover:opacity-90 ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}