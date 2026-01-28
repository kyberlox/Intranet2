export const createMail = (text: string, signature: string, postCard: boolean) => {
    return `
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {
                    margin: 0;
                    padding: 20px;
                    font-family: Arial, sans-serif;
                    background-color: #f9f9f9;
                    color: #333;
                    line-height: 1.5;
                }
                
                .container {
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 30px;
                    border: 1px solid #ddd;
                }
                
                .text {
                    margin-bottom: 30px;
                    white-space: pre-line;
                }
                
                .postcard {
                    text-align: center;
                    margin: 30px 0;
                }
                
                .postcard img {
                    max-width: 100%;
                    height: auto;
                    border: 1px solid #eee;
                }
                
                .logo {
                    text-align: center;
                    margin: 30px 0;
                }
                
                .logo img {
                    width: 200px;
                    height: auto;
                }
                
                .signature {
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #eee;
                    font-size: 14px;
                    color: #666;
                    white-space: pre-line;
                }
                
                @media (max-width: 600px) {
                    body {
                        padding: 10px;
                    }
                    
                    .container {
                        padding: 20px;
                    }
                    
                    .logo img {
                        width: 150px;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="text">
                    ${text}
                </div>
                
              ${postCard ? `<div class="postcard">
                    <img src="cid:file_logo" alt="Поздравительная открытка">
                </div>` : ''}
                
                <div class="signature">
                    ${signature}
                </div>

                <div class="logo">
                    <img src="cid:company_logo" alt="Логотип компании">
                </div>
            </div>
        </body>
        </html>
    `;
}