import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { fetchBoardDetails } from '../../redux/boards';
import { editCard, deleteCard } from '../../redux/cards';
import CardModal from '../CardModal/CardModal';
import { useModal } from '../../context/Modal';
import './Card.css';

const Card = ({ card, sectionId, boardId }) => {
   const dispatch = useDispatch();
   const { setModalContent } = useModal();
   const [isDeleting, setIsDeleting] = useState(false);

   const openCardModal = () => {
      setModalContent(<CardModal card={card} boardId={boardId} />);
   };

   const handleDeleteCard = async (e) => {
      e.stopPropagation(); // Prevent opening the card modal

      if (isDeleting) return;

      if (
         window.confirm(
            `Are you sure you want to delete the card "${card.name}"?`,
         )
      ) {
         setIsDeleting(true);

         try {
            await dispatch(deleteCard(card.id));
            
            dispatch(fetchBoardDetails(boardId)); // Refresh the board data to update UI
         } catch (error) {
            alert('Failed to delete card. Please try again.');
         } finally {
            setIsDeleting(false);
         }
      }
   };

   // Format due date if exists
   const formattedDueDate = card.dueDate
      ? new Date(card.dueDate).toLocaleDateString()
      : null;

   return (
      <div className="card" onClick={openCardModal}>
         <div className="card-header">
            <div className="card-title">{card.name}</div>
            <button
               className="delete-card-button"
               onClick={handleDeleteCard}
               disabled={isDeleting}
               title="Delete Card"
            >
               ×
            </button>
         </div>

         {card.labels && (
            <div className="card-labels">
               <span className="label">{card.labels}</span>
            </div>
         )}

         {card.description && (
            <div className="card-description-preview">
               {card.description.length > 100
                  ? card.description.substring(0, 100) + '...'
                  : card.description}
            </div>
         )}

         {formattedDueDate && (
            <div className="card-due-date">Due: {formattedDueDate}</div>
         )}
      </div>
   );
};

export default Card;
