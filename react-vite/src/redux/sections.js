// Action Types
const LOAD_SECTIONS = 'sections/LOAD_SECTIONS';
const ADD_SECTION = 'sections/ADD_SECTION';
const UPDATE_SECTION = 'sections/UPDATE_SECTION';
const REMOVE_SECTION = 'sections/REMOVE_SECTION';

// Action Creators
const loadSections = (sections) => ({
   type: LOAD_SECTIONS,
   payload: sections,
});

const addSection = (section) => ({
   type: ADD_SECTION,
   payload: section,
});

const updateSection = (section) => ({
   type: UPDATE_SECTION,
   payload: section,
});

const removeSection = (sectionId) => ({
   type: REMOVE_SECTION,
   payload: sectionId,
});

// Thunks
export const fetchBoardSections = (boardId) => async (dispatch) => {
   try {
      const response = await fetch(`/api/boards/${boardId}/sections`);

      if (response.ok) {
         const data = await response.json();
         dispatch(loadSections(data.sections));
         return data;
      } else {
         const errors = await response.json();
         return errors;
      }
   } catch (error) {
      return { error: 'Failed to fetch sections' };
   }
};

export const createSection = (boardId, sectionData) => async (dispatch) => {
   try {
      const response = await fetch(`/api/boards/${boardId}/sections`, {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify(sectionData),
      });

      if (response.ok) {
         const data = await response.json();
         dispatch(addSection(data.section));
         return data;
      } else {
         const errors = await response.json();
         return errors;
      }
   } catch (error) {
      return { error: 'Failed to create section' };
   }
};

export const editSection = (sectionId, sectionData) => async (dispatch) => {
   try {
      const response = await fetch(`/api/card-sections/${sectionId}`, {
         method: 'PUT',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify(sectionData),
      });

      if (response.ok) {
         const data = await response.json();
         dispatch(updateSection(data));
         return data;
      } else {
         const errors = await response.json();
         return errors;
      }
   } catch (error) {
      return { error: 'Failed to update section' };
   }
};

export const deleteSection = (sectionId) => async (dispatch) => {
   try {
      const response = await fetch(`/api/card-sections/${sectionId}`, {
         method: 'DELETE',
      });

      if (response.ok) {
         dispatch(removeSection(sectionId));
         return { message: 'Section deleted successfully' };
      } else {
         const errors = await response.json();
         return errors;
      }
   } catch (error) {
      return { error: 'Failed to delete section' };
   }
};

// Initial State
const initialState = {
   boardSections: {},
};

// Reducer
const sectionsReducer = (state = initialState, action) => {
   let newState;

   switch (action.type) {
      case LOAD_SECTIONS:
         newState = { ...state, boardSections: {} };
         action.payload.forEach((section) => {
            newState.boardSections[section.id] = section;
         });
         return newState;

      case ADD_SECTION:
         return {
            ...state,
            boardSections: {
               ...state.boardSections,
               [action.payload.id]: action.payload,
            },
         };

      case UPDATE_SECTION:
         return {
            ...state,
            boardSections: {
               ...state.boardSections,
               [action.payload.id]: action.payload,
            },
         };

      case REMOVE_SECTION:
         newState = {
            ...state,
            boardSections: { ...state.boardSections },
         };
         delete newState.boardSections[action.payload];
         return newState;

      default:
         return state;
   }
};

export default sectionsReducer;
