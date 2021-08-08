import "./App.css";
import LoginPage from "./pages/login";
import { Switch, Route } from "react-router-dom";
import RegisterPage from "./pages/register";
import LoginSuccessPage from "./pages/login_success";
import WebchatPage from "./pages/webchat";
import UserSkills from "./pages/user_skills";

function App() {
  document.title = "IT Career Bot"
  return (
    <div className="App">
      <Switch>
        <Route path="/login">
          <LoginPage />
        </Route>

        <Route path="/register">
          <RegisterPage />
        </Route>

        <Route path="/login_success">
          <LoginSuccessPage />
        </Route>

        <Route path="/user/skills">
          <UserSkills/>
        </Route>

        <Route path="/">
          <WebchatPage />
        </Route>
      </Switch>
    </div>
  );
}

export default App;
