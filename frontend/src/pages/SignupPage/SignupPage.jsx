import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { Link } from "react-router-dom";
import "../LoginPage/AuthPage.css";
import SignUpForm from '../../components/SignUpForm/SignUpForm';
import Logo from '../../assets/logo.png';

export default function AuthPage() {
  
  return (
    <div className="mt-24 page-wrapper">
      <header className="flex justify-center items-center mt-6">
        <img src={ Logo } alt="NeuroFlowLogo" className="w-24 h-24 sm:w-32 sm:h-32 md:w-40 md:h-40 lg:w-48 lg:h-48" />
      </header>
      <main>
        <section className="content-wrapper -mt-14">
            <SignUpForm />
            <p className="other-page">
                Already have an account? 
                <Link to="/login" className="other-page-link">Sign in</Link>
            </p>
        </section>
      </main>
      <footer className="oai-footer">
        <p className="footer-text">Created by: Abhay Singh, Andrew Ho, Dylan Tran, and John Vu</p>
      </footer>
    </div>
  );
}