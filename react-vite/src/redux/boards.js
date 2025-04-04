// Action Types
const LOAD_BOARDS = 'boards/LOAD_BOARDS';
const ADD_BOARD = 'boards/ADD_BOARD';
const UPDATE_BOARD = 'boards/UPDATE_BOARD';
const REMOVE_BOARD = 'boards/REMOVE_BOARD';

// Action Creators
const loadBoards = (boards) => ({
   type: LOAD_BOARDS,
   payload: boards,
});

const addBoard = (board) => ({
   type: ADD_BOARD,
   payload: board,
});

const updateBoard = (board) => ({
   type: UPDATE_BOARD,
   payload: board,
});

const removeBoard = (boardId) => ({
   type: REMOVE_BOARD,
   payload: boardId,
});

// Thunks
export const fetchBoards = () => async (dispatch) => {
   try {
      const response = await fetch('/api/boards');

      if (response.ok) {
         const data = await response.json();
         dispatch(loadBoards(data.boards));
         return data;
      } else {
         const errors = await response.json();
         return errors;
      }
   } catch (error) {
      return { error: 'Failed to fetch boards' };
   }
};

export const fetchBoardDetails = (boardId) => async (dispatch) => {
   try {
      const response = await fetch(`/api/boards/${boardId}`);

      if (response.ok) {
         const data = await response.json();
         dispatch(updateBoard(data));
         return data;
      } else {
         const errors = await response.json();
         return errors;
      }
   } catch (error) {
      return { error: 'Failed to fetch board details' };
   }
};

export const createBoard = (boardData) => async (dispatch) => {
   try {
      const response = await fetch('/api/boards', {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify(boardData),
      });

      if (response.ok) {
         const data = await response.json();
         dispatch(addBoard(data.board));
         return data;
      } else {
         const errors = await response.json();
         return errors;
      }
   } catch (error) {
      return { error: 'Failed to create board' };
   }
};

export const editBoard = (boardId, boardData) => async (dispatch) => {
   try {
      const response = await fetch(`/api/boards/${boardId}`, {
         method: 'PUT',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify(boardData),
      });

      if (response.ok) {
         const data = await response.json();
         dispatch(updateBoard(data.board));
         return data;
      } else {
         const errors = await response.json();
         return errors;
      }
   } catch (error) {
      return { error: 'Failed to update board' };
   }
};

export const deleteBoard = (boardId) => async (dispatch) => {
   try {
      const response = await fetch(`/api/boards/${boardId}`, {
         method: 'DELETE',
      });

      if (response.ok) {
         dispatch(removeBoard(boardId));
         return { message: 'Board deleted successfully' };
      } else {
         const errors = await response.json();
         return errors;
      }
   } catch (error) {
      return { error: 'Failed to delete board' };
   }
};

// Initial State
const initialState = {
   allBoards: {},
   singleBoard: null,
};

// Reducer
const boardsReducer = (state = initialState, action) => {
   let newState;

   switch (action.type) {
      case LOAD_BOARDS:
         newState = { ...state, allBoards: {} };
         action.payload.forEach((board) => {
            newState.allBoards[board.id] = board;
         });
         return newState;

      case ADD_BOARD:
         return {
            ...state,
            allBoards: {
               ...state.allBoards,
               [action.payload.id]: action.payload,
            },
         };

      case UPDATE_BOARD:
         return {
            ...state,
            allBoards: {
               ...state.allBoards,
               [action.payload.id]: action.payload,
            },
            singleBoard: action.payload,
         };

      case REMOVE_BOARD:
         newState = {
            ...state,
            allBoards: { ...state.allBoards },
         };
         delete newState.allBoards[action.payload];
         if (state.singleBoard && state.singleBoard.id === action.payload) {
            newState.singleBoard = null;
         }
         return newState;

      default:
         return state;
   }
};

export default boardsReducer;
