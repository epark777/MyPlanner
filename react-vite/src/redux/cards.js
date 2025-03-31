// Action Types
const LOAD_CARDS = 'cards/LOAD_CARDS';
const ADD_CARD = 'cards/ADD_CARD';
const UPDATE_CARD = 'cards/UPDATE_CARD';
const REMOVE_CARD = 'cards/REMOVE_CARD';
const REORDER_CARDS = 'cards/REORDER_CARDS';

// Action Creators
const loadCards = (sectionId, cards) => ({
  type: LOAD_CARDS,
  payload: { sectionId, cards }
});

const addCard = (card) => ({
  type: ADD_CARD,
  payload: card
});

const updateCard = (card) => ({
  type: UPDATE_CARD,
  payload: card
});

const removeCard = (cardId) => ({
  type: REMOVE_CARD,
  payload: cardId
});

const reorderCardsAction = (cards) => ({
  type: REORDER_CARDS,
  payload: cards
});

// Thunks
export const fetchSectionCards = (sectionId) => async (dispatch) => {
  try {
    const response = await fetch(`/api/card-sections/${sectionId}/cards`);
    
    if (response.ok) {
      const data = await response.json();
      dispatch(loadCards(sectionId, data.cards));
      return data;
    } else {
      const errors = await response.json();
      return errors;
    }
  } catch (error) {
    return { error: 'Failed to fetch cards' };
  }
};

export const createCard = (sectionId, cardData) => async (dispatch) => {
  try {
    const response = await fetch(`/api/card-sections/${sectionId}/cards`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(cardData)
    });
    
    if (response.ok) {
      const data = await response.json();
      dispatch(addCard(data));
      return data;
    } else {
      const errors = await response.json();
      return errors;
    }
  } catch (error) {
    return { error: 'Failed to create card' };
  }
};

export const editCard = (cardId, cardData) => async (dispatch) => {
  try {
    const response = await fetch(`/api/cards/${cardId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(cardData)
    });
    
    if (response.ok) {
      const data = await response.json();
      dispatch(updateCard(data));
      return data;
    } else {
      const errors = await response.json();
      return errors;
    }
  } catch (error) {
    return { error: 'Failed to update card' };
  }
};

export const deleteCard = (cardId) => async (dispatch) => {
  try {
    const response = await fetch(`/api/cards/${cardId}`, {
      method: 'DELETE'
    });
    
    if (response.ok) {
      dispatch(removeCard(cardId));
      return { message: 'Card deleted successfully' };
    } else {
      const errors = await response.json();
      return errors;
    }
  } catch (error) {
    return { error: 'Failed to delete card' };
  }
};

export const reorderCards = (cardsData) => async (dispatch) => {
  try {
    const response = await fetch('/api/cards/reorder', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reorderedCards: cardsData })
    });
    
    if (response.ok) {
      const data = await response.json();
      dispatch(reorderCardsAction(data.cards));
      return data;
    } else {
      const errors = await response.json();
      return errors;
    }
  } catch (error) {
    return { error: 'Failed to reorder cards' };
  }
};

// Initial State
const initialState = {
  sectionCards: {},
  allCards: {}
};

// Reducer
const cardsReducer = (state = initialState, action) => {
  let newState;
  
  switch (action.type) {
    case LOAD_CARDS:
      newState = { 
        ...state,
        sectionCards: {
          ...state.sectionCards,
          [action.payload.sectionId]: action.payload.cards
        },
        allCards: { ...state.allCards }
      };
      
      action.payload.cards.forEach(card => {
        newState.allCards[card.id] = card;
      });
      
      return newState;
    
    case ADD_CARD:
      return {
        ...state,
        allCards: {
          ...state.allCards,
          [action.payload.id]: action.payload
        },
        sectionCards: {
          ...state.sectionCards,
          [action.payload.cardSectionId]: [
            ...(state.sectionCards[action.payload.cardSectionId] || []),
            action.payload
          ]
        }
      };
    
    case UPDATE_CARD:
      return {
        ...state,
        allCards: {
          ...state.allCards,
          [action.payload.id]: action.payload
        }
      };
    
    case REMOVE_CARD:
      newState = {
        ...state,
        allCards: { ...state.allCards },
        sectionCards: { ...state.sectionCards }
      };
      
      const cardToRemove = state.allCards[action.payload];
      if (cardToRemove) {
        const sectionId = cardToRemove.cardSectionId;
        if (state.sectionCards[sectionId]) {
          newState.sectionCards[sectionId] = state.sectionCards[sectionId]
            .filter(card => card.id !== action.payload);
        }
        delete newState.allCards[action.payload];
      }
      
      return newState;
    
    case REORDER_CARDS:
      newState = {
        ...state,
        allCards: { ...state.allCards },
        sectionCards: { ...state.sectionCards }
      };
      
      action.payload.forEach(card => {
        if (newState.allCards[card.id]) {
          newState.allCards[card.id] = {
            ...newState.allCards[card.id],
            order: card.order,
            cardSectionId: card.cardSectionId
          };
        }
      });
      
      return newState;
    
    default:
      return state;
  }
};

export default cardsReducer;