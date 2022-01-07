import { createStore, applyMiddleware } from "redux";
import { rootReducer } from "../Reducer/index";
import thunk from "redux-thunk";

export default function configureStore(initialState) {
    const createStoreWithMiddleware = applyMiddleware(thunk)(createStore);
    const store = createStoreWithMiddleware(rootReducer);
    return store;
}
