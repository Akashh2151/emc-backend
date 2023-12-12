from flask import Blueprint, jsonify, request
from model.rating_model import RatingInfo
from werkzeug.utils import secure_filename
from controller.shop import storage_client
import traceback  # Import traceback module

rating = Blueprint('rating', __name__)

@rating.route('/rating', methods=['POST'])
def userrating():
    try:
        data = request.form
        print("Received data:", data)
        rating_value = int(data.get('rating_value'))
        comment = data.get('comment')
        
        # Validate rating value
        if rating_value > 5:
            response = {'Body': None, 'error': 'Rating value cannot be greater than 5', 'status_code': 400}
            return jsonify(response)
        
                # Validate comment length
        min_comment_length = 10  # Adjust the minimum length as needed
        if not comment or len(comment) < min_comment_length:
            response = {'Body': None, 'error': f'Comment must be at least {min_comment_length} characters long', 'status_code': 400}
            return jsonify(response)
        

        if not rating_value or not comment:
            response = {'Body': None, 'error': 'All fields are required', 'status_code': 400}
            return jsonify(response)

        if 'images' not in request.files:
            response = {'error': 'Images are required', 'status_code': 400}
            return jsonify(response)

        images = request.files.getlist('images')

        total_size = sum(len(imagesfile.read()) for imagesfile in images)
        if total_size > 10 * 1024 * 1024:
            return jsonify({'error': 'Total image size exceeds 5MB'}), 400

        # Save each image to Firebase Storage and collect URLs
        photo_urls = []
        for image_file in images:
            image_file.seek(0)
            filename = secure_filename(image_file.filename)
            blob = storage_client.blob('rating/img/' + filename)

            # Set content type to image/jpeg
            blob.upload_from_file(image_file, content_type='image/jpeg')

            # Set ACL to public-read
            blob.acl.all().grant_read()

            photo_urls.append(blob.public_url)

        rating_info = RatingInfo(rating=rating_value, comment=comment, photos=photo_urls)
        rating_info.save()

        # Include photo URLs in the response
        response = {'Body': {'photo_urls': photo_urls}, 'status': 'success', 'statusCode': 200,
                    'message': 'User rating successfully submitted'}
        return jsonify(response)

    except Exception as e:
        # Print the traceback to identify the specific error
        traceback.print_exc()
        return jsonify({'error': str(e), 'status_code': 500}), 500