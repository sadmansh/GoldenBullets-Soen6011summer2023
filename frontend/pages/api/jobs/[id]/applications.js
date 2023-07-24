export default async (req, res) => {
	try {
		// Get access token from authorization header
		const authHeader = req.headers.authorization
		if (!authHeader) {
			return res.status(401).json({ message: 'Authorization header missing' })
		}
		if (req.method === 'GET') {
			// Get the job post ID from the URL
			const { id } = req.query
			// Send a GET request to the API to fetch all applications for the job post
			const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/jobs/${id}/applications`, {
				method: 'GET',
				headers: {
					Authorization: authHeader,
					'Content-Type': 'application/json',
				},
			})
			const data = await response.json()
			if (response.ok) {
				return res.status(200).json(data)
			}
		} else {
			return res.status(405).json({ message: 'Method not allowed' })
		}
	} catch (error) {
		console.error('Error accessing api/jobs/[id]/apply', error)
		return res.status(403).json({ message: 'User forbidden' })
	}
}