// Action Types
const LOAD_FAVORITES = 'favorites/LOAD_FAVORITES';
const ADD_FAVORITE = 'favorites/ADD_FAVORITE';
const REMOVE_FAVORITE = 'favorites/REMOVE_FAVORITE';

// Action Creators
const loadFavorites = (favorites) => ({
   type: LOAD_FAVORITES,
   payload: favorites,
});

const addFavorite = (favorite) => ({
   type: ADD_FAVORITE,
   payload: favorite,
});

const removeFavorite = (favoriteId) => ({
   type: REMOVE_FAVORITE,
   payload: favoriteId,
});

// Thunks
export const fetchFavorites = () => async (dispatch) => {
   try {
      const response = await fetch('/api/favorites');

      if (response.ok) {
         const data = await response.json();
         dispatch(loadFavorites(data));
         return data;
      } else {
         const errors = await response.json();
         return errors;
      }
   } catch (error) {
      return { error: 'Failed to fetch favorites' };
   }
};

export const createFavorite = (boardId) => async (dispatch) => {
   try {
      const response = await fetch('/api/favorites', {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify({ board_id: boardId }),
      });

      if (response.ok) {
         const data = await response.json();
         dispatch(addFavorite(data));
         return data;
      } else {
         const errors = await response.json();
         return errors;
      }
   } catch (error) {
      return { error: 'Failed to add favorite' };
   }
};

export const deleteFavorite = (favoriteId) => async (dispatch) => {
   try {
      const response = await fetch(`/api/favorites/${favoriteId}`, {
         method: 'DELETE',
      });

      if (response.ok) {
         dispatch(removeFavorite(favoriteId));
         return { message: 'Favorite removed successfully' };
      } else {
         const errors = await response.json();
         return errors;
      }
   } catch (error) {
      return { error: 'Failed to remove favorite' };
   }
};

// Initial State
const initialState = {
   userFavorites: {},
};

// Reducer
const favoritesReducer = (state = initialState, action) => {
   let newState;

   switch (action.type) {
      case LOAD_FAVORITES:
         newState = { ...state, userFavorites: {} };
         action.payload.forEach((favorite) => {
            newState.userFavorites[favorite.id] = favorite;
         });
         return newState;

      case ADD_FAVORITE:
         return {
            ...state,
            userFavorites: {
               ...state.userFavorites,
               [action.payload.id]: action.payload,
            },
         };

      case REMOVE_FAVORITE:
         newState = {
            ...state,
            userFavorites: { ...state.userFavorites },
         };
         delete newState.userFavorites[action.payload];
         return newState;

      default:
         return state;
   }
};

export default favoritesReducer;
