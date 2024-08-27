import ButtonGradient from "../assets/svg/ButtonGradient.jsx"
import Header from '../components/Header.jsx'
import Hero from '../components/Hero.jsx';

const Home = () => {
  return (
    <>
      <div className="pt-[4.75rem] lg:pt-[5.25rem] overflow-hidden">
        <Header />
        <Hero />
      </div>
      <ButtonGradient />
    </>
  );
};

export default Home