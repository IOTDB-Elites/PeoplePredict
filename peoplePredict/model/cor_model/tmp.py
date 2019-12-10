from peoplePredict.database.dao import Dao

# a = np.array([[1,2],[3,4]])
# # k = np.array([0,2])
# # b = np.array([3,7])
# # print(a)
# # print(k)
# # print(b)
# # print(((a.T*k) + b).T)

def upload_data():
    DATABASE = 'correlation_drop'
    dao = Dao()
    cache = []
    count = 0
    # dao.clear_database(DATABASE)
    data = {'month': 9, 'day': 29, 'hour': 7, 'lng_gcj02': 108.977, 'lat_gcj02': 34.249, 'value': 225}, {'month': 9,
                                                                                                         'day': 30,
                                                                                                         'hour': 7,
                                                                                                         'lng_gcj02': 108.977,
                                                                                                         'lat_gcj02': 34.249,
                                                                                                         'value': 230}, {
               'month': 9, 'day': 24, 'hour': 7, 'lng_gcj02': 108.986, 'lat_gcj02': 34.352, 'value': 230}, {'month': 9,
                                                                                                            'day': 25,
                                                                                                            'hour': 7,
                                                                                                            'lng_gcj02': 108.986,
                                                                                                            'lat_gcj02': 34.352,
                                                                                                            'value': 229}, {
               'month': 9, 'day': 26, 'hour': 7, 'lng_gcj02': 108.986, 'lat_gcj02': 34.352, 'value': 228}, {'month': 9,
                                                                                                            'day': 27,
                                                                                                            'hour': 7,
                                                                                                            'lng_gcj02': 108.986,
                                                                                                            'lat_gcj02': 34.352,
                                                                                                            'value': 227}, {
               'month': 9, 'day': 28, 'hour': 7, 'lng_gcj02': 108.986, 'lat_gcj02': 34.352, 'value': 226}, {'month': 9,
                                                                                                            'day': 29,
                                                                                                            'hour': 7,
                                                                                                            'lng_gcj02': 108.986,
                                                                                                            'lat_gcj02': 34.352,
                                                                                                            'value': 225}, {
               'month': 9, 'day': 30, 'hour': 7, 'lng_gcj02': 108.986, 'lat_gcj02': 34.352, 'value': 231}, {'month': 9,
                                                                                                            'day': 24,
                                                                                                            'hour': 7,
                                                                                                            'lng_gcj02': 108.987,
                                                                                                            'lat_gcj02': 34.23,
                                                                                                            'value': 229}, {
               'month': 9, 'day': 25, 'hour': 7, 'lng_gcj02': 108.987, 'lat_gcj02': 34.23, 'value': 228}, {'month': 9,
                                                                                                           'day': 26,
                                                                                                           'hour': 7,
                                                                                                           'lng_gcj02': 108.987,
                                                                                                           'lat_gcj02': 34.23,
                                                                                                           'value': 227}, {
               'month': 9, 'day': 27, 'hour': 7, 'lng_gcj02': 108.987, 'lat_gcj02': 34.23, 'value': 227}, {'month': 9,
                                                                                                           'day': 28,
                                                                                                           'hour': 7,
                                                                                                           'lng_gcj02': 108.987,
                                                                                                           'lat_gcj02': 34.23,
                                                                                                           'value': 226}, {
               'month': 9, 'day': 29, 'hour': 7, 'lng_gcj02': 108.987, 'lat_gcj02': 34.23, 'value': 225}, {'month': 9,
                                                                                                           'day': 30,
                                                                                                           'hour': 7,
                                                                                                           'lng_gcj02': 108.987,
                                                                                                           'lat_gcj02': 34.23,
                                                                                                           'value': 230}, {
               'month': 9, 'day': 24, 'hour': 7, 'lng_gcj02': 109.016, 'lat_gcj02': 34.296, 'value': 235}, {'month': 9,
                                                                                                            'day': 25,
                                                                                                            'hour': 7,
                                                                                                            'lng_gcj02': 109.016,
                                                                                                            'lat_gcj02': 34.296,
                                                                                                            'value': 234}, {
               'month': 9, 'day': 26, 'hour': 7, 'lng_gcj02': 109.016, 'lat_gcj02': 34.296, 'value': 233}, {'month': 9,
                                                                                                            'day': 27,
                                                                                                            'hour': 7,
                                                                                                            'lng_gcj02': 109.016,
                                                                                                            'lat_gcj02': 34.296,
                                                                                                            'value': 232}, {
               'month': 9, 'day': 28, 'hour': 7, 'lng_gcj02': 109.016, 'lat_gcj02': 34.296, 'value': 231}, {'month': 9,
                                                                                                            'day': 29,
                                                                                                            'hour': 7,
                                                                                                            'lng_gcj02': 109.016,
                                                                                                            'lat_gcj02': 34.296,
                                                                                                            'value': 230}, {
               'month': 9, 'day': 30, 'hour': 7, 'lng_gcj02': 109.016, 'lat_gcj02': 34.296, 'value': 236}, {'month': 9,
                                                                                                            'day': 24,
                                                                                                            'hour': 7,
                                                                                                            'lng_gcj02': 109.041,
                                                                                                            'lat_gcj02': 34.242,
                                                                                                            'value': 229}, {
               'month': 9, 'day': 25, 'hour': 7, 'lng_gcj02': 109.041, 'lat_gcj02': 34.242, 'value': 228}, {'month': 9,
                                                                                                            'day': 26,
                                                                                                            'hour': 7,
                                                                                                            'lng_gcj02': 109.041,
                                                                                                            'lat_gcj02': 34.242,
                                                                                                            'value': 227}, {
               'month': 9, 'day': 27, 'hour': 7, 'lng_gcj02': 109.041, 'lat_gcj02': 34.242, 'value': 226}, {'month': 9,
                                                                                                            'day': 28,
                                                                                                            'hour': 7,
                                                                                                            'lng_gcj02': 109.041,
                                                                                                            'lat_gcj02': 34.242,
                                                                                                            'value': 226}, {
               'month': 9, 'day': 29, 'hour': 7, 'lng_gcj02': 109.041, 'lat_gcj02': 34.242, 'value': 225}, {'month': 9,
                                                                                                            'day': 30,
                                                                                                            'hour': 7,
                                                                                                            'lng_gcj02': 109.041,
                                                                                                            'lat_gcj02': 34.242,
                                                                                                            'value': 230}, {
               'month': 9, 'day': 24, 'hour': 7, 'lng_gcj02': 109.064, 'lat_gcj02': 34.347, 'value': 235}, {'month': 9,
                                                                                                            'day': 25,
                                                                                                            'hour': 7,
                                                                                                            'lng_gcj02': 109.064,
                                                                                                            'lat_gcj02': 34.347,
                                                                                                            'value': 234}, {
               'month': 9, 'day': 26, 'hour': 7, 'lng_gcj02': 109.064, 'lat_gcj02': 34.347, 'value': 233}, {'month': 9,
                                                                                                            'day': 27,
                                                                                                            'hour': 7,
                                                                                                            'lng_gcj02': 109.064,
                                                                                                            'lat_gcj02': 34.347,
                                                                                                            'value': 232}, {
               'month': 9, 'day': 28, 'hour': 7, 'lng_gcj02': 109.064, 'lat_gcj02': 34.347, 'value': 231}, {'month': 9,
                                                                                                            'day': 29,
                                                                                                            'hour': 7,
                                                                                                            'lng_gcj02': 109.064,
                                                                                                            'lat_gcj02': 34.347,
                                                                                                            'value': 230}, {
               'month': 9, 'day': 30, 'hour': 7, 'lng_gcj02': 109.064, 'lat_gcj02': 34.347, 'value': 236}, {'month': 9,
                                                                                                            'day': 24,
                                                                                                            'hour': 7,
                                                                                                            'lng_gcj02': 108.85,
                                                                                                            'lat_gcj02': 34.316,
                                                                                                            'value': 219}, {
               'month': 9, 'day': 25, 'hour': 7, 'lng_gcj02': 108.85, 'lat_gcj02': 34.316, 'value': 218}, {'month': 9,
                                                                                                           'day': 26,
                                                                                                           'hour': 7,
                                                                                                           'lng_gcj02': 108.85,
                                                                                                           'lat_gcj02': 34.316,
                                                                                                           'value': 217}, {
               'month': 9, 'day': 27, 'hour': 7, 'lng_gcj02': 108.85, 'lat_gcj02': 34.316, 'value': 216}, {'month': 9,
                                                                                                           'day': 28,
                                                                                                           'hour': 7,
                                                                                                           'lng_gcj02': 108.85,
                                                                                                           'lat_gcj02': 34.316,
                                                                                                           'value': 215}, {
               'month': 9, 'day': 29, 'hour': 7, 'lng_gcj02': 108.85, 'lat_gcj02': 34.316, 'value': 214}, {'month': 9,
                                                                                                           'day': 30,
                                                                                                           'hour': 7,
                                                                                                           'lng_gcj02': 108.85,
                                                                                                           'lat_gcj02': 34.316,
                                                                                                           'value': 220}, {
               'month': 9, 'day': 24, 'hour': 7, 'lng_gcj02': 108.892, 'lat_gcj02': 34.209, 'value': 219}, {'month': 9,
                                                                                                            'day': 25,
                                                                                                            'hour': 7,
                                                                                                            'lng_gcj02': 108.892,
                                                                                                            'lat_gcj02': 34.209,
                                                                                                            'value': 218}, {
               'month': 9, 'day': 26, 'hour': 7, 'lng_gcj02': 108.892, 'lat_gcj02': 34.209, 'value': 217}, {'month': 9,
                                                                                                            'day': 27,
                                                                                                            'hour': 7,
                                                                                                            'lng_gcj02': 108.892,
                                                                                                            'lat_gcj02': 34.209,
                                                                                                            'value': 216}, {
               'month': 9, 'day': 28, 'hour': 7, 'lng_gcj02': 108.892, 'lat_gcj02': 34.209, 'value': 215}, {'month': 9,
                                                                                                            'day': 29,
                                                                                                            'hour': 7,
                                                                                                            'lng_gcj02': 108.892,
                                                                                                            'lat_gcj02': 34.209,
                                                                                                            'value': 214}, {
               'month': 9, 'day': 30, 'hour': 7, 'lng_gcj02': 108.892, 'lat_gcj02': 34.209, 'value': 220}, {'month': 9,
                                                                                                            'day': 24,
                                                                                                            'hour': 7,
                                                                                                            'lng_gcj02': 108.991,
                                                                                                            'lat_gcj02': 34.328,
                                                                                                            'value': 161}, {
               'month': 9, 'day': 25, 'hour': 7, 'lng_gcj02': 108.991, 'lat_gcj02': 34.328, 'value': 161}, {'month': 9,
                                                                                                            'day': 26,
                                                                                                            'hour': 7,
                                                                                                            'lng_gcj02': 108.991,
                                                                                                            'lat_gcj02': 34.328,
                                                                                                            'value': 160}, {
               'month': 9, 'day': 27, 'hour': 7, 'lng_gcj02': 108.991, 'lat_gcj02': 34.328, 'value': 160}, {'month': 9,
                                                                                                            'day': 28,
                                                                                                            'hour': 7,
                                                                                                            'lng_gcj02': 108.991,
                                                                                                            'lat_gcj02': 34.328,
                                                                                                            'value': 159}, {
               'month': 9, 'day': 29, 'hour': 7, 'lng_gcj02': 108.991, 'lat_gcj02': 34.328, 'value': 158}, {'month': 9,
                                                                                                            'day': 30,
                                                                                                            'hour': 7,
                                                                                                            'lng_gcj02': 108.991,
                                                                                                            'lat_gcj02': 34.328,
                                                                                                            'value': 162}, {
               'month': 9, 'day': 24, 'hour': 7, 'lng_gcj02': 108.955, 'lat_gcj02': 34.26, 'value': 187}, {'month': 9,
                                                                                                           'day': 25,
                                                                                                           'hour': 7,
                                                                                                           'lng_gcj02': 108.955,
                                                                                                           'lat_gcj02': 34.26,
                                                                                                           'value': 186}, {
               'month': 9, 'day': 26, 'hour': 7, 'lng_gcj02': 108.955, 'lat_gcj02': 34.26, 'value': 185}, {'month': 9,
                                                                                                           'day': 27,
                                                                                                           'hour': 7,
                                                                                                           'lng_gcj02': 108.955,
                                                                                                           'lat_gcj02': 34.26,
                                                                                                           'value': 184}, {
               'month': 9, 'day': 28, 'hour': 7, 'lng_gcj02': 108.955, 'lat_gcj02': 34.26, 'value': 183}, {'month': 9,
                                                                                                           'day': 29,
                                                                                                           'hour': 7,
                                                                                                           'lng_gcj02': 108.955,
                                                                                                           'lat_gcj02': 34.26,
                                                                                                           'value': 182}, {
               'month': 9, 'day': 30, 'hour': 7, 'lng_gcj02': 108.955, 'lat_gcj02': 34.26, 'value': 188}, {'month': 9,
                                                                                                           'day': 24,
                                                                                                           'hour': 7,
                                                                                                           'lng_gcj02': 108.8,
                                                                                                           'lat_gcj02': 34.274,
                                                                                                           'value': 223}, {
               'month': 9, 'day': 25, 'hour': 7, 'lng_gcj02': 108.8, 'lat_gcj02': 34.274, 'value': 222}, {'month': 9,
                                                                                                          'day': 26,
                                                                                                          'hour': 7,
                                                                                                          'lng_gcj02': 108.8,
                                                                                                          'lat_gcj02': 34.274,
                                                                                                          'value': 221}, {
               'month': 9, 'day': 27, 'hour': 7, 'lng_gcj02': 108.8, 'lat_gcj02': 34.274, 'value': 220}, {'month': 9,
                                                                                                          'day': 28,
                                                                                                          'hour': 7,
                                                                                                          'lng_gcj02': 108.8,
                                                                                                          'lat_gcj02': 34.274,
                                                                                                          'value': 219}, {
               'month': 9, 'day': 29, 'hour': 7, 'lng_gcj02': 108.8, 'lat_gcj02': 34.274, 'value': 218}, {'month': 9,
                                                                                                          'day': 30,
                                                                                                          'hour': 7,
                                                                                                          'lng_gcj02': 108.8,
                                                                                                          'lat_gcj02': 34.274,
                                                                                                          'value': 224}, {
               'month': 9, 'day': 24, 'hour': 7, 'lng_gcj02': 108.869, 'lat_gcj02': 34.318, 'value': 161}, {'month': 9,
                                                                                                            'day': 25,
                                                                                                            'hour': 7,
                                                                                                            'lng_gcj02': 108.869,
                                                                                                            'lat_gcj02': 34.318,
                                                                                                            'value': 161}, {
               'month': 9, 'day': 26, 'hour': 7, 'lng_gcj02': 108.869, 'lat_gcj02': 34.318, 'value': 160}, {'month': 9,
                                                                                                            'day': 27,
                                                                                                            'hour': 7,
                                                                                                            'lng_gcj02': 108.869,
                                                                                                            'lat_gcj02': 34.318,
                                                                                                            'value': 160}, {
               'month': 9, 'day': 28, 'hour': 7, 'lng_gcj02': 108.869, 'lat_gcj02': 34.318, 'value': 159}, {'month': 9,
                                                                                                            'day': 29,
                                                                                                            'hour': 7,
                                                                                                            'lng_gcj02': 108.869,
                                                                                                            'lat_gcj02': 34.318,
                                                                                                            'value': 158}, {
               'month': 9, 'day': 30, 'hour': 7, 'lng_gcj02': 108.869, 'lat_gcj02': 34.318, 'value': 162}, {'month': 9,
                                                                                                            'day': 24,
                                                                                                            'hour': 12,
                                                                                                            'lng_gcj02': 108.786,
                                                                                                            'lat_gcj02': 34.218,
                                                                                                            'value': 0}, {
               'month': 9, 'day': 25, 'hour': 12, 'lng_gcj02': 108.786, 'lat_gcj02': 34.218, 'value': 0}, {'month': 9,
                                                                                                           'day': 26,
                                                                                                           'hour': 12,
                                                                                                           'lng_gcj02': 108.786,
                                                                                                           'lat_gcj02': 34.218,
                                                                                                           'value': 0}, {
               'month': 9, 'day': 27, 'hour': 12, 'lng_gcj02': 108.786, 'lat_gcj02': 34.218, 'value': 0}, {'month': 9,
                                                                                                           'day': 28,
                                                                                                           'hour': 12,
                                                                                                           'lng_gcj02': 108.786,
                                                                                                           'lat_gcj02': 34.218,
                                                                                                           'value': 0}, {
               'month': 9, 'day': 29, 'hour': 12, 'lng_gcj02': 108.786, 'lat_gcj02': 34.218, 'value': 0}, {'month': 9,
                                                                                                           'day': 30,
                                                                                                           'hour': 12,
                                                                                                           'lng_gcj02': 108.786,
                                                                                                           'lat_gcj02': 34.218,
                                                                                                           'value': 0}, {
               'month': 9, 'day': 24, 'hour': 12, 'lng_gcj02': 108.786, 'lat_gcj02': 34.219, 'value': 200}, {'month': 9,
                                                                                                             'day': 25,
                                                                                                             'hour': 12,
                                                                                                             'lng_gcj02': 108.786,
                                                                                                             'lat_gcj02': 34.219,
                                                                                                             'value': 199}, {
               'month': 9, 'day': 26, 'hour': 12, 'lng_gcj02': 108.786, 'lat_gcj02': 34.219, 'value': 197}, {'month': 9,
                                                                                                             'day': 27,
                                                                                                             'hour': 12,
                                                                                                             'lng_gcj02': 108.786,
                                                                                                             'lat_gcj02': 34.219,
                                                                                                             'value': 196}, {
               'month': 9, 'day': 28, 'hour': 12, 'lng_gcj02': 108.786, 'lat_gcj02': 34.219, 'value': 195}, {'month': 9,
                                                                                                             'day': 29,
                                                                                                             'hour': 12,
                                                                                                             'lng_gcj02': 108.786,
                                                                                                             'lat_gcj02': 34.219,
                                                                                                             'value': 194}, {
               'month': 9, 'day': 30, 'hour': 12, 'lng_gcj02': 108.786, 'lat_gcj02': 34.219, 'value': 201}, {'month': 9,
                                                                                                             'day': 24,
                                                                                                             'hour': 12,
                                                                                                             'lng_gcj02': 108.786,
                                                                                                             'lat_gcj02': 34.223,
                                                                                                             'value': 0}, {
               'month': 9, 'day': 25, 'hour': 12, 'lng_gcj02': 108.786, 'lat_gcj02': 34.223, 'value': 0}, {'month': 9,
                                                                                                           'day': 26,
                                                                                                           'hour': 12,
                                                                                                           'lng_gcj02': 108.786,
                                                                                                           'lat_gcj02': 34.223,
                                                                                                           'value': 0}, {
               'month': 9, 'day': 27, 'hour': 12, 'lng_gcj02': 108.786, 'lat_gcj02': 34.223, 'value': 0}, {'month': 9,
                                                                                                           'day': 28,
                                                                                                           'hour': 12,
                                                                                                           'lng_gcj02': 108.786,
                                                                                                           'lat_gcj02': 34.223,
                                                                                                           'value': 0}, {
               'month': 9, 'day': 29, 'hour': 12, 'lng_gcj02': 108.786, 'lat_gcj02': 34.223, 'value': 0}, {'month': 9,
                                                                                                           'day': 30,
                                                                                                           'hour': 12,
                                                                                                           'lng_gcj02': 108.786,
                                                                                                           'lat_gcj02': 34.223,
                                                                                                           'value': 0}

    for i in data:
        cache.append(i)
        if len(cache) == 10:
            count += 10
            try:
                dao.insert_many(DATABASE, cache)
            except:
                print(cache)
                exit(-1)
            cache.clear()
            if count % 10 == 0:
                print(count)
    if len(cache) != 0:
        dao.insert_many(DATABASE, cache)
    dao.close()

if __name__ == '__main__':
    upload_data()