import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { useModal } from '../../context/Modal';
import { createBoard } from '../../redux/boards';
import './BoardModals.css';

const CreateBoardModal = () => {
   const dispatch = useDispatch();
   const { closeModal } = useModal();
   const [name, setName] = useState('');
   const [errors, setErrors] = useState({});

   const handleSubmit = async (e) => {
      e.preventDefault();
      setErrors({});

      if (!name.trim()) {
         setErrors({ name: 'Board name is required' });
         return;
      }

      const response = await dispatch(createBoard({ name }));

      if (response && response.error) {
         setErrors(response.details || { name: response.message });
      } else {
         closeModal();
      }
   };

   return (
      <div className="board-modal">
         <h2>Create New Board</h2>
         <form onSubmit={handleSubmit}>
            <div className="form-group">
               <label htmlFor="board-name">Board Name</label>
               <input
                  id="board-name"
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Enter board name"
                  maxLength={50}
               />
               {errors.name && <p className="error">{errors.name}</p>}
            </div>
            <div className="modal-buttons">
               <button
                  type="button"
                  onClick={closeModal}
                  className="cancel-button"
               >
                  Cancel
               </button>
               <button type="submit" className="submit-button">
                  Create Board
               </button>
            </div>
         </form>
      </div>
   );
};

export default CreateBoardModal;
