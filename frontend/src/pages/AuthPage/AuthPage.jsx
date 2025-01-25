import { useState } from 'react';
import '../AuthPage/AuthPage.css';
import SignUpForm from '../../components/SignUpForm/SignUpForm';
import SignInForm from '../../components/SignInForm/SignInForm';
import Logo from '../../assets/logo.png';

export default function AuthPage({ setUser }) {
  const [showSignUp, setShowSignUp] = useState(false);

  return (
    <div className="page-wrapper">
      <header className="flex justify-center items-center mt-6">
        <img src={ Logo } alt="NeuroFlowLogo" className="w-24 h-24 sm:w-32 sm:h-32 md:w-40 md:h-40 lg:w-48 lg:h-48" />
      </header>
      <main>
        <section className="content-wrapper -mt-14">
            { showSignUp ?
                <SignUpForm setUser={setUser} />
                :
                <SignInForm setUser={setUser} />
            }
            <p className="other-page">
                Already have an account? 
                <span className="other-page-link" onClick={() => setShowSignUp(!showSignUp)}>{showSignUp ? 'Log In' : 'Sign Up'}</span>
            </p>
        </section>
      </main>
      <footer className="oai-footer">
        <p className="footer-text">Created by: Abhay Singh, Andrew Ho, Dylan Tran, and John Vu</p>
      </footer>
    </div>
  );
}