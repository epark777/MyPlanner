import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { useModal } from '../../context/Modal';
import { editCard } from '../../redux/cards';
import { fetchBoardDetails } from '../../redux/boards';
import './CardModal.css';

const CardModal = ({ card, boardId }) => {
   const dispatch = useDispatch();
   const { closeModal } = useModal();

   const [formState, setFormState] = useState({
      name: card.name || '',
      description: card.description || '',
      labels: card.labels || '',
      dueDate: card.dueDate
         ? new Date(card.dueDate).toISOString().split('T')[0]
         : '',
   });

   const [errors, setErrors] = useState({});
   const [isSaving, setIsSaving] = useState(false);

   const handleInputChange = (e) => {
      const { name, value } = e.target;
      setFormState((prev) => ({
         ...prev,
         [name]: value,
      }));
   };

   const handleSubmit = async (e) => {
      e.preventDefault();
      setErrors({});

      // Validate required fields
      if (!formState.name.trim()) {
         setErrors((prev) => ({ ...prev, name: 'Card title is required' }));
         return;
      }

      setIsSaving(true);

      try {
         const response = await dispatch(editCard(card.id, formState));

         if (response && response.error) {
            setErrors({ form: response.message || 'Failed to update card' });
            setIsSaving(false);
            return;
         }

         // Refresh board data
         await dispatch(fetchBoardDetails(boardId));
         closeModal();
      } catch (error) {
         setErrors({ form: 'An unexpected error occurred' });
         setIsSaving(false);
      }
   };

   return (
      <div className="card-modal">
         <form onSubmit={handleSubmit}>
            <div className="form-group">
               <label htmlFor="name">Title</label>
               <input
                  id="name"
                  name="name"
                  type="text"
                  value={formState.name}
                  onChange={handleInputChange}
                  placeholder="Enter card title"
                  maxLength={50}
               />
               {errors.name && <p className="error">{errors.name}</p>}
            </div>

            <div className="form-group">
               <label htmlFor="description">Description</label>
               <textarea
                  id="description"
                  name="description"
                  value={formState.description}
                  onChange={handleInputChange}
                  placeholder="Enter card description"
                  rows={5}
                  maxLength={500}
               />
            </div>

            <div className="form-group">
               <label htmlFor="labels">Labels</label>
               <input
                  id="labels"
                  name="labels"
                  type="text"
                  value={formState.labels}
                  onChange={handleInputChange}
                  placeholder="Enter labels (comma separated)"
                  maxLength={50}
               />
            </div>

            <div className="form-group">
               <label htmlFor="dueDate">Due Date</label>
               <input
                  id="dueDate"
                  name="dueDate"
                  type="date"
                  value={formState.dueDate}
                  onChange={handleInputChange}
               />
            </div>

            {errors.form && <p className="error form-error">{errors.form}</p>}

            <div className="modal-buttons">
               <button
                  type="button"
                  onClick={closeModal}
                  className="cancel-button"
                  disabled={isSaving}
               >
                  Cancel
               </button>
               <button
                  type="submit"
                  className="save-button"
                  disabled={isSaving}
               >
                  {isSaving ? 'Saving...' : 'Save Changes'}
               </button>
            </div>
         </form>
      </div>
   );
};

export default CardModal;
