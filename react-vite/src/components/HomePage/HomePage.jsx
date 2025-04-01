import { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { fetchBoards } from '../../redux/boards';
import { fetchFavorites } from '../../redux/favorites';
import CreateBoardModal from '../BoardModals/CreateBoardModal';
import OpenModalButton from '../OpenModalButton';
import './HomePage.css';

const HomePage = () => {
   const dispatch = useDispatch();
   const navigate = useNavigate();
   const user = useSelector((state) => state.session.user);
   const allBoards = useSelector((state) => state.boards.allBoards);
   const favorites = useSelector((state) => state.favorites.userFavorites);
   const [isLoaded, setIsLoaded] = useState(false);

   useEffect(() => {
      const loadData = async () => {
         await Promise.all([
            dispatch(fetchBoards()),
            dispatch(fetchFavorites()),
         ]);
         setIsLoaded(true);
      };

      if (user) {
         loadData();
      }
   }, [dispatch, user]);

   if (!user) {
      return (
         <div className="homepage">
            <div className="homepage-hero">
               <h1>Welcome to TaskBoard</h1>
               <p>
                  Organize your tasks, manage your projects, and boost your
                  productivity.
               </p>
               <p>Please log in or sign up to get started.</p>
            </div>
         </div>
      );
   }

   if (!isLoaded) {
      return <div>Loading...</div>;
   }

   const boardsArray = Object.values(allBoards);
   const favoritesArray = Object.values(favorites);

   return (
      <div className="homepage">
         <div className="homepage-header">
            <h1>Your Boards</h1>
            <OpenModalButton
               buttonText="Create New Board"
               modalComponent={<CreateBoardModal />}
            />
         </div>

         {favoritesArray.length > 0 && (
            <div className="favorite-boards-section">
               <h2>Favorite Boards</h2>
               <div className="boards-grid">
                  {favoritesArray.map((favorite) => (
                     <div
                        key={favorite.id}
                        className="board-card"
                        onClick={() => navigate(`/boards/${favorite.Board.id}`)}
                     >
                        <h3>{favorite.Board.name}</h3>
                     </div>
                  ))}
               </div>
            </div>
         )}

         <div className="all-boards-section">
            <h2>All Boards</h2>
            {boardsArray.length === 0 ? (
               <p>
                  You don't have any boards yet. Create your first board to get
                  started!
               </p>
            ) : (
               <div className="boards-grid">
                  {boardsArray.map((board) => (
                     <div
                        key={board.id}
                        className="board-card"
                        onClick={() => navigate(`/boards/${board.id}`)}
                     >
                        <h3>{board.name}</h3>
                     </div>
                  ))}
               </div>
            )}
         </div>
      </div>
   );
};

export default HomePage;
