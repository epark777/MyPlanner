import { NavLink } from 'react-router-dom';
import { useSelector } from 'react-redux';
import ProfileButton from './ProfileButton';
import OpenModalButton from '../OpenModalButton';
import CreateBoardModal from '../BoardModals/CreateBoardModal';
import './Navigation.css';

function Navigation({ isLoaded }) {
  const sessionUser = useSelector((state) => state.session.user);

  return (
    <div className="navbar">
      <NavLink to="/" className="logo">
        <span>MyPlanner</span>
      </NavLink>

      <div className="right-side">
        {isLoaded ? (
          sessionUser ? (
            <>
              <OpenModalButton
                buttonText="Create Board"
                modalComponent={<CreateBoardModal />}
                className="create-board-button"
              />
              <ProfileButton user={sessionUser} />
            </>
          ) : (
            <>
              <NavLink to="/signup" className="signup-button">
                Sign Up
              </NavLink>
              <NavLink to="/login" className="login-button">
                Log In
              </NavLink>
            </>
          )
        ) : (
          <ProfileButton className='nav-profile-icon' />
        )}
      </div>
    </div>
  );
}

export default Navigation;