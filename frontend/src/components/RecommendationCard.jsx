import {
  ArrowRight,
  Sparkles
} from "lucide-react";


function RecommendationCard({
  priority,
  title,
  description,
  saving,
  confidence,
  metric,
  onSimulate
}) {

  return (
    <div className={`recommendation ${priority}`}>

      <div className="recommendation-header">

        <div className="recommendation-priority">
          {priority}
        </div>

        <div className="confidence">
          {confidence}% confidence
        </div>

      </div>


      <h3>{title}</h3>

      <p>
        {description}
      </p>


      <div className="recommendation-impact">

        <div>
          <span>MODELED BENEFIT</span>
          <strong>{saving}</strong>
        </div>

        <div>
          <span>EXPECTED CHANGE</span>
          <strong>{metric}</strong>
        </div>

      </div>


      <div className="recommendation-actions">

        <button
          className="primary-action"
          onClick={onSimulate}
        >
          <Sparkles size={15} />

          Simulate

          <ArrowRight size={15} />
        </button>

        <button className="secondary-action">
          Why?
        </button>

      </div>

    </div>
  );
}

export default RecommendationCard;