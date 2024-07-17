import { createBrowserRouter, createRoutesFromElements, Route } from "react-router-dom";
import Home from "../pages/Home";
import Conversation from "../pages/Conversation";
import LandingPageLayout from "../layouts/LandingPageLayout";
import CombinedConversationPage from "../pages/CombinedConversationPage";
import NewsSourcesPage from "../pages/NewsSourcesPage";
import ImageDisplay from "../components/ImageDisplay";

export const routes = createBrowserRouter(
    createRoutesFromElements(
        <Route >
            <Route path="/" element={<LandingPageLayout />}>
                <Route index element={<Home />} />
                <Route path='conversation' element={<Conversation />} />
                <Route path='combined-conversation' element={<CombinedConversationPage />} />
                <Route path='Sources' element={<NewsSourcesPage />} />
                <Route path='visuals' element={<ImageDisplay />} />
            </Route>

        </Route >
    )
)