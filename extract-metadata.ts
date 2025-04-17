import type { VercelRequest, VercelResponse } from '@vercel/node';

// Vercel serverless function to extract CV metadata (mock implementation)
export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Parse multipart form data (for file upload)
  // Vercel Node functions không hỗ trợ parsing multipart natively, nên dùng 'busboy' hoặc trả về mock nếu không cần xử lý file thật
  // Ở đây trả về mock metadata để frontend hoạt động

  // Nếu bạn cần xử lý file thật, hãy dùng thư viện 'busboy' với req
  // Ví dụ đơn giản:
  // const busboy = new Busboy({ headers: req.headers });
  // busboy.on('file', (fieldname, file, filename, encoding, mimetype) => { ... })

  // Trả về mock metadata
  const metadata = {
    name: 'Nguyen Van A',
    email: 'nguyenvana@example.com',
    phone: '+84 912345678',
    experience: '3 years',
    skills: ['React', 'Node.js', 'TypeScript'],
    fileName: 'cv_sample.pdf',
    uploadedAt: new Date().toISOString(),
  };
  return res.status(200).json({ metadata });
}
