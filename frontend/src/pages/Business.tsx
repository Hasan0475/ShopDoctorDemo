export default function Business() {
  return (
    <>
      <h2 className="sec">Business model — free check-up, paid follow-up care</h2>
      <p className="sub">The free check-up brings owners in; Pro follow-up is the main revenue.</p>
      <div className="price">
        <div className="plan">
          <h3>Free</h3>
          <div className="role">Brings owners in</div>
          <div className="amt">HK$0</div>
          <ul>
            <li>Shop Health Score</li>
            <li>Profit check per dish</li>
            <li>Twin-shop benchmark</li>
          </ul>
        </div>
        <div className="plan featured">
          <h3>Pro · Follow-Up Care</h3>
          <div className="role">Main revenue</div>
          <div className="amt">HK$999<small> / month</small></div>
          <ul>
            <li>Price Simulator</li>
            <li>Shop Doctor Chat</li>
            <li>Marketing Kit: menus, posts, photos</li>
            <li>Monthly follow-up &amp; plan adjustments</li>
          </ul>
        </div>
        <div className="plan">
          <h3>Future · Referral</h3>
          <div className="role">HK$ ___ per tenant</div>
          <div className="amt">TBD</div>
          <ul>
            <li>Ghost &amp; shared kitchen referrals</li>
            <li>JF Kitchen</li>
            <li>247 ShareKitchen</li>
            <li>Freshlane Hong Kong</li>
          </ul>
        </div>
      </div>

      <h2 className="sec" style={{ marginTop: 40, fontSize: 20 }}>Implementation timeline</h2>
      <p className="sub">From HACK4SDG prototype to 1,000 owners.</p>
      <div className="timeline">
        <div className="tl"><div className="when">Oct 2026</div><h4>Hackathon</h4><p>Working prototype · user testing · owner interviews · ideation</p></div>
        <div className="tl"><div className="when">Nov 2026 – Mar 2027</div><h4>Pilot</h4><p>10+ owners · import real data · apply for HKSTP</p></div>
        <div className="tl"><div className="when">Apr – Sep 2027</div><h4>Launch</h4><p>Pro model live · target 100+ shops · kitchen partners</p></div>
        <div className="tl"><div className="when">Oct 2028+</div><h4>Scale</h4><p>Profit · target 1,000+ shops</p></div>
      </div>

      <h2 className="sec" style={{ marginTop: 40, fontSize: 20 }}>Funding &amp; budget (1st year)</h2>
      <div className="twins">
        <div className="card"><div className="pad">
          <h3 style={{ marginTop: 0 }}>Funding sources</h3>
          <div className="twin"><div className="list">
            <div className="item"><span>Cyberport Creative Micro Fund</span><b>up to HK$100k / 6 mo</b></div>
            <div className="item"><span>HKSTP Ideathon Programme</span><b>up to HK$100k / 1 yr</b></div>
            <div className="item"><span>HACK4SDG</span><b>hopefully! 🤞</b></div>
          </div></div>
        </div></div>
        <div className="card"><div className="pad">
          <h3 style={{ marginTop: 0 }}>Projections</h3>
          <div className="twin"><div className="list">
            <div className="item"><span>Pro tier revenue at launch</span><b>up to HK$999k / mo</b></div>
            <div className="item"><span>Break-even</span><b>5 Pro shops</b></div>
            <div className="item"><span>First year</span><b>funded by grants</b></div>
          </div></div>
        </div></div>
      </div>
    </>
  );
}
