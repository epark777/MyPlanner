import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { fetchBoardDetails } from '../../redux/boards';
import { createSection } from '../../redux/sections';
import { EditBoardModal, DeleteBoardModal } from '../BoardModals';
import CardSection from '../CardSection/CardSection';
import OpenModalButton from '../OpenModalButton';
import './BoardPage.css';

const BoardPage = () => {
   const { boardId } = useParams();
   const navigate = useNavigate();
   const dispatch = useDispatch();
   const [isLoaded, setIsLoaded] = useState(false);
   const [newSectionTitle, setNewSectionTitle] = useState('');
   const [sectionError, setSectionError] = useState('');
   const [isAddingSectionVisible, setIsAddingSectionVisible] = useState(false);

   const board = useSelector((state) => state.boards.singleBoard);
   const user = useSelector((state) => state.session.user);

   // Load board data
   useEffect(() => {
      const loadBoard = async () => {
         if (!user) return;

         const response = await dispatch(fetchBoardDetails(boardId));
         if (response && response.error) {
            navigate('/'); // Handle error - board not found or unauthorized
         }
         setIsLoaded(true);
      };

      loadBoard();
   }, [dispatch, boardId, navigate, user]);

   if (!user) {
      navigate('/login');
      return null;
   }

   if (!isLoaded) {
      return <div className="loading">Loading board...</div>;
   }

   if (!board) {
      return (
         <div className="not-found">
            Board not found or you do not have access to it.
         </div>
      );
   }

   const handleAddSection = async (e) => {
      e.preventDefault();
      setSectionError('');

      if (!newSectionTitle.trim()) {
         setSectionError('Section title is required');
         return;
      }

      const response = await dispatch(
         createSection(boardId, { title: newSectionTitle }),
      );
      if (response && response.error) {
         setSectionError(response.message || 'Failed to create section');
      } else {
         setNewSectionTitle('');
         setIsAddingSectionVisible(false);

         dispatch(fetchBoardDetails(boardId)); // Refresh board to get the new section
      }
   };

   const cancelAddSection = () => {
      setNewSectionTitle('');
      setSectionError('');
      setIsAddingSectionVisible(false);
   };

   return (
      <div className="board-page">
         <div className="board-header">
            <div className="board-title-section">
               <button className="back-button" onClick={() => navigate('/')}>
                  ← Back to Boards
               </button>
               <h1>{board.name}</h1>
            </div>
            <div className="board-actions">
               <OpenModalButton
                  buttonText="Edit"
                  modalComponent={<EditBoardModal board={board} />}
               />
               <OpenModalButton
                  buttonText="Delete"
                  modalComponent={<DeleteBoardModal board={board} />}
               />
            </div>
         </div>

         <div className="board-sections">
            {board.CardSections && board.CardSections.length > 0 ? (
               board.CardSections.map((section) => (
                  <CardSection
                     key={section.id}
                     section={section}
                     boardId={boardId}
                  />
               ))
            ) : (
               <div className="no-sections">
                  <p>This board does not have any sections yet.</p>
               </div>
            )}

            {isAddingSectionVisible ? (
               <div className="add-section-form">
                  <form onSubmit={handleAddSection}>
                     <input
                        type="text"
                        value={newSectionTitle}
                        onChange={(e) => setNewSectionTitle(e.target.value)}
                        placeholder="Enter section title"
                        maxLength={50}
                        autoFocus
                     />
                     {sectionError && <p className="error">{sectionError}</p>}
                     <div className="form-buttons">
                        <button type="button" onClick={cancelAddSection}>
                           Cancel
                        </button>
                        <button type="submit">Add Section</button>
                     </div>
                  </form>
               </div>
            ) : (
               <button
                  className="add-section-button"
                  onClick={() => setIsAddingSectionVisible(true)}
               >
                  + Add Section
               </button>
            )}
         </div>
      </div>
   );
};

export default BoardPage;
