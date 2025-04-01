import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { useModal } from '../../context/Modal';
import { deleteBoard } from '../../redux/boards';
import './BoardModals.css';

const DeleteBoardModal = ({ board }) => {
   const dispatch = useDispatch();
   const navigate = useNavigate();
   const { closeModal } = useModal();
   const [isDeleting, setIsDeleting] = useState(false);
   const [error, setError] = useState('');

   const handleDelete = async () => {
      setIsDeleting(true);
      setError('');

      try {
         const response = await dispatch(deleteBoard(board.id));

         if (response && response.error) {
            setError(response.message || 'Failed to delete board');
            setIsDeleting(false);
         } else {
            closeModal();
            navigate('/');
         }
      } catch (err) {
         setError('An unexpected error occurred');
         setIsDeleting(false);
      }
   };

   return (
      <div className="board-modal">
         <h2>Delete Board</h2>
         <p>
            Are you sure you want to delete <strong>{board.name}</strong>?
         </p>
         <p className="warning">
            This action cannot be undone. All cards and sections in this board
            will be permanently deleted.
         </p>

         {error && <p className="error">{error}</p>}

         <div className="modal-buttons">
            <button
               type="button"
               onClick={closeModal}
               className="cancel-button"
               disabled={isDeleting}
            >
               Cancel
            </button>
            <button
               type="button"
               onClick={handleDelete}
               className="delete-button"
               disabled={isDeleting}
            >
               {isDeleting ? 'Deleting...' : 'Delete Board'}
            </button>
         </div>
      </div>
   );
};

export default DeleteBoardModal;
