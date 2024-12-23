queries_templates = {
    'sql_select_categories' : """SELECT `CategoryID`, `CategoryName`, `Description` FROM Categories c ORDER BY c.`Ordering`""",
    'sql_select_category_by_id' : """SELECT `CategoryID`, `CategoryName`, `Description`, `Ordering` FROM Categories c WHERE c.CategoryID=%s""",
    'sql_create_category': """ INSERT INTO `Categories` (`CategoryName`, `Description`, `Ordering`) VALUES (%s, %s, %s) """,
    'sql_delete_cateory': """DELETE FROM `Categories` WHERE CategoryID=%s""",
    'sql_update_category': """UPDATE Categories SET CategoryName=%s, Description=%s, Ordering=%s WHERE CategoryID=%s""",
    
    'sql_select_images': """SELECT `ImageID`, `ImageURL`, `Ordering` FROM Images i WHERE i.CategoryID = %s ORDER BY i.Ordering""",
    'sql_select_images_by_category_id': """SELECT `CategoryID`, `ImageID`, `ImageURL`, `Ordering` FROM Images i WHERE i.CategoryID = %s ORDER BY i.Ordering""",
    'sql_select_images_by_image_and_category_id': """SELECT `CategoryID`, `ImageID`, `ImageURL` FROM Images i WHERE i.CategoryID = %s AND i.ImageID = %s""",
    
    'sql_create_images' :"""INSERT INTO `Images` (`CategoryID`, `ImageURL`) VALUES (%s, %s);""",
    'sql_delete_image_by_image_and_category_id': """DELETE FROM Images i WHERE i.CategoryID = %s AND i.ImageID = %s""",
    'sql_update_image_order' : """UPDATE `Images` SET `Ordering`=%s WHERE `ImageID`=%s AND `CategoryID` =%s""",
}