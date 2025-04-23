import { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { NavLink, useNavigate } from 'react-router-dom';
import { fetchBoards } from '../../redux/boards';
import { fetchFavorites } from '../../redux/favorites';
import OpenModalButton from '../OpenModalButton';
import CreateBoardModal from '../BoardModals/CreateBoardModal';
import './HomePage.css';

function HomePage() {
  const sessionUser = useSelector((state) => state.session.user);
  const allBoards = useSelector(state => state.boards.allBoards);
  const favorites = useSelector(state => state.favorites.userFavorites);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (sessionUser) {
      Promise.all([
        dispatch(fetchBoards()),
        dispatch(fetchFavorites())
      ])
        .then(() => {
          setLoading(false);
        })
        .catch((err) => {
          console.error('Error fetching data:', err);
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  }, [dispatch, sessionUser]);

  if (loading) {
    return <div className="loading-container">Loading...</div>;
  }

  if (sessionUser) {
    const boardsArray = Object.values(allBoards);
    const favoritesArray = Object.values(favorites);

    return (
      <div className="homepage">
        <div className="homepage-content">
          <div className="homepage-header">
            <h1>Your Boards</h1>
            <OpenModalButton
              buttonText="Create New Board"
              modalComponent={<CreateBoardModal />}
              className="button create-button"
            />
          </div>

          {favoritesArray.length > 0 && (
            <div className="favorite-boards-section">
              <h2>Favorite Boards</h2>
              <div className="boards-grid">
                {favoritesArray.map(favorite => (
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
              <p>You do not have any boards yet. Create your first board to get started!</p>
            ) : (
              <div className="boards-grid">
                {boardsArray.map(board => (
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
      </div>
    );
  }

  return (
    <div className="homepage">
      <div className="homepage-content">
        <h1>Welcome to MyPlanner</h1>
        <p>
          Organize your tasks, manage your projects, and boost your productivity.
        </p>
        <div className="homepage-buttons">
          <NavLink to="/signup" className="button signup-button">
            Sign Up
          </NavLink>
          <NavLink to="/login" className="button login-button">
            Log In
          </NavLink>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
