import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { fetchBoardDetails } from '../../redux/boards';
import { editSection, deleteSection } from '../../redux/sections';
import { createCard } from '../../redux/cards';
import Card from '../Card/Card';
import './CardSection.css';

const CardSection = ({ section, boardId }) => {
   const dispatch = useDispatch();
   const [isEditingTitle, setIsEditingTitle] = useState(false);
   const [sectionTitle, setSectionTitle] = useState(section.title);
   const [isAddingCard, setIsAddingCard] = useState(false);
   const [newCardName, setNewCardName] = useState('');
   const [errors, setErrors] = useState({});

   // Handle title edit
   const handleTitleEdit = async () => {
      if (!sectionTitle.trim()) {
         setErrors({ title: 'Section title cannot be empty' });
         return;
      }

      if (sectionTitle === section.title) {
         setIsEditingTitle(false);
         return;
      }

      const response = await dispatch(
         editSection(section.id, { title: sectionTitle }),
      );
      if (response && response.error) {
         setErrors({
            title: response.message || 'Failed to update section title',
         });
      } else {
         setIsEditingTitle(false);
         setErrors({});
      }
   };

   // Handle section deletion
   const handleSectionDelete = async () => {
      if (
         window.confirm(
            `Are you sure you want to delete the section "${section.title}" and all its cards?`,
         )
      ) {
         const response = await dispatch(deleteSection(section.id));
         if (response && response.error) {
            setErrors({
               section: response.message || 'Failed to delete section',
            });
         } else {
            
            dispatch(fetchBoardDetails(boardId)); // Refresh board to update UI
         }
      }
   };

   // Handle card creation
   const handleAddCard = async (e) => {
      e.preventDefault();
      setErrors({});

      if (!newCardName.trim()) {
         setErrors({ card: 'Card title is required' });
         return;
      }

      const response = await dispatch(
         createCard(section.id, { name: newCardName }),
      );
      if (response && response.error) {
         setErrors({ card: response.message || 'Failed to create card' });
      } else {
         setNewCardName('');
         setIsAddingCard(false);
         
         dispatch(fetchBoardDetails(boardId)); // Refresh board to update UI
      }
   };

   const cards = section.Cards || [];

   return (
      <div className="card-section">
         <div className="section-header">
            {isEditingTitle ? (
               <div className="edit-title-form">
                  <input
                     type="text"
                     value={sectionTitle}
                     onChange={(e) => setSectionTitle(e.target.value)}
                     onBlur={handleTitleEdit}
                     onKeyDown={(e) => e.key === 'Enter' && handleTitleEdit()}
                     autoFocus
                     maxLength={50}
                  />
                  {errors.title && <p className="error">{errors.title}</p>}
               </div>
            ) : (
               <div className="section-title-container">
                  <h2 onClick={() => setIsEditingTitle(true)}>
                     {section.title}
                  </h2>
                  <div className="section-actions">
                     <button
                        className="delete-section-button"
                        onClick={handleSectionDelete}
                        title="Delete Section"
                     >
                        ×
                     </button>
                  </div>
               </div>
            )}
         </div>

         <div className="cards-container">
            {cards.length > 0 ? (
               cards.map((card) => (
                  <Card
                     key={card.id}
                     card={card}
                     sectionId={section.id}
                     boardId={boardId}
                  />
               ))
            ) : (
               <p className="no-cards">No cards in this section</p>
            )}
         </div>

         {errors.section && (
            <p className="error section-error">{errors.section}</p>
         )}

         {isAddingCard ? (
            <div className="add-card-form">
               <form onSubmit={handleAddCard}>
                  <input
                     type="text"
                     value={newCardName}
                     onChange={(e) => setNewCardName(e.target.value)}
                     placeholder="Enter card title"
                     autoFocus
                     maxLength={50}
                  />
                  {errors.card && <p className="error">{errors.card}</p>}
                  <div className="form-buttons">
                     <button
                        type="button"
                        onClick={() => {
                           setIsAddingCard(false);
                           setNewCardName('');
                           setErrors({});
                        }}
                     >
                        Cancel
                     </button>
                     <button type="submit">Add Card</button>
                  </div>
               </form>
            </div>
         ) : (
            <button
               className="add-card-button"
               onClick={() => setIsAddingCard(true)}
            >
               + Add Card
            </button>
         )}
      </div>
   );
};

export default CardSection;
