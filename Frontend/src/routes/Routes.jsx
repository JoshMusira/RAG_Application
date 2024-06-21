import { createBrowserRouter, createRoutesFromElements, Route } from "react-router-dom";
import Home from "../pages/Home";
import Conversation from "../pages/Conversation";
import LandingPageLayout from "../layouts/LandingPageLayout";

export const routes = createBrowserRouter(
    createRoutesFromElements(
        <Route >
            <Route path="/" element={<LandingPageLayout />}>
                <Route index element={<Home />} />
                <Route path='conversation' element={<Conversation />} />
            </Route>

        </Route >
    )
)