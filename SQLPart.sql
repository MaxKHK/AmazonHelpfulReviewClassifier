select top 20 * from 
	dbo.metadata as m
	join [dbo].[ReviewsCleanCSV] as r on m.asin = r.asin

	select top 20 r.helpful, count(r.helpful) from 
	dbo.metadata as m
	join [dbo].[ReviewsCleanCSV] as r on m.asin = r.asin
	group by r.helpful
	order by count(r.helpful) desc, r.helpful desc



select top 100000
	m.asin,
	m.price,
	r.reviewerID,
	r.reviewText,
	r.reviewOrig,
	len(r.reviewText) as LenReview,
	r.Summary,
	len(r.Summary) as LenSummary,
	r.overall,
	r.helpful
from
	dbo.metadata as m
	join [dbo].[ReviewsCleanCSV] as r on m.asin = r.asin