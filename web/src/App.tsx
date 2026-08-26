import { Footer } from "./components/Footer";
import { PromoBar } from "./components/Landing";
import { Navbar } from "./components/Navbar";
import { useRoute } from "./app/router";
import { Home } from "./pages/Home";
import { AccountPage } from "./pages/Account";
import { AccountsPage } from "./pages/Accounts";
import { AdminUsersPage } from "./pages/AdminUsers";
import { IntelligencePage } from "./pages/Intelligence";
import { RiskPage } from "./pages/Risk";
import { ContactPage } from "./pages/Contact";
import { DashboardPage } from "./pages/Dashboard";
import { ForgotPasswordPage, LoginPage, RegisterPage } from "./pages/Auth";
import {
  AboutPage,
  ChallengesPage,
  FaqPage,
  HowItWorksPage,
  LegalPage,
  NotFoundPage,
  PayoutsPage,
  PlatformPage,
} from "./pages/Static";

function renderRoute(path: string) {
  if (path.startsWith("/legal/")) return <LegalPage which={path.replace("/legal/", "")} />;

  switch (path) {
    case "/":
      return <Home />;
    case "/challenges":
      return <ChallengesPage />;
    case "/how-it-works":
      return <HowItWorksPage />;
    case "/platform":
      return <PlatformPage />;
    case "/payouts":
      return <PayoutsPage />;
    case "/faq":
      return <FaqPage />;
    case "/about":
      return <AboutPage />;
    case "/contact":
      return <ContactPage />;
    case "/login":
      return <LoginPage />;
    case "/register":
      return <RegisterPage />;
    case "/forgot-password":
      return <ForgotPasswordPage />;
    case "/dashboard":
      return <DashboardPage />;
    case "/account":
      return <AccountPage />;
    case "/accounts":
      return <AccountsPage />;
    case "/risk":
      return <RiskPage />;
    case "/intelligence":
      return <IntelligencePage />;
    case "/admin/users":
      return <AdminUsersPage />;
    default:
      return <NotFoundPage />;
  }
}

export function App() {
  const [path] = useRoute();

  return (
    <>
      <div className="aurora" aria-hidden="true" />
      <div className="grid-lines" aria-hidden="true" />
      <div id="app">
        <PromoBar />
        <Navbar />
        <main>{renderRoute(path)}</main>
        <Footer />
      </div>
    </>
  );
}
