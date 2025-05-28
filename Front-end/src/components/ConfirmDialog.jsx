// components/ConfirmDialog.jsx
import React, { useState, createContext, useContext, useRef } from "react";

const ConfirmDialogContext = createContext();

export const ConfirmDialogProvider = ({ children }) => {
  const [dialog, setDialog] = useState({
    isOpen: false,
    message: "",
    onConfirm: null,
    onCancel: null,
  });

  const resolveRef = useRef(null);
  const rejectRef = useRef(null);

  const confirm = (message) => {
    return new Promise((resolve, reject) => {
      setDialog({
        isOpen: true,
        message,
        onConfirm: () => {
          setDialog({ ...dialog, isOpen: false });
          resolve(true);
        },
        onCancel: () => {
          setDialog({ ...dialog, isOpen: false });
          resolve(false); // Resolve with false if cancelled
        },
      });
    });
  };

  return (
    <ConfirmDialogContext.Provider value={{ confirm }}>
      {children}
      {dialog.isOpen && (
        <div className="confirm-dialog-overlay">
          <div className="confirm-dialog">
            <p>{dialog.message}</p>
            <div className="confirm-dialog-actions">
              <button onClick={dialog.onConfirm}>Ya</button>
              <button onClick={dialog.onCancel} className="cancel-button">
                Tidak
              </button>
            </div>
          </div>
        </div>
      )}
    </ConfirmDialogContext.Provider>
  );
};

export const useConfirmDialog = () => useContext(ConfirmDialogContext);
