# xls.py
"""
bento_xls.py
Import experimental data in Matlab Bento xls (Excel spreadsheet) format
into Python Bento's database, using SQLAlchemy and xlrd.
"""

from db.schema_sqlalchemy import Session
from sqlalchemy.sql.expression import null
import xlrd
import sqlalchemy as sa
from db.schema_sqlalchemy import *
from timecode import Timecode
from datetime import datetime
from video.seqIo import seqIo_reader
from os.path import abspath, dirname, isdir, sep

def import_common_info(xls_sheet, directory):
    """
    Import common items from the first row of the spreadsheet
    """
    common_data = {}

    cell_0_0 = xls_sheet.cell(0,0)
    base_dir = directory
    if cell_0_0.ctype == xlrd.XL_CELL_TEXT:
        if isdir(cell_0_0.value):
            base_dir = cell_0_0.value
        else:
            print(f"Path specified for base_directory, {cell_0_0.value}, does not exist; using default")

    common_data['base_directory'] = base_dir
    common_data['neural_framerate'] = float(xls_sheet.cell_value(0, 2))
    common_data['annotation_framerate'] = float(xls_sheet.cell_value(0, 4))
    common_data['multiple_neural_trials_per_file'] = bool(xls_sheet.cell_value(0, 6))
    common_data['multiple_annotation_trials_per_file'] = bool(xls_sheet.cell_value(0, 8))
    common_data['has_behavior_movies'] = bool(xls_sheet.cell_value(0, 10))
    common_data['annotation_offset'] = float(xls_sheet.cell_value(0, 12))
    common_data['has_tracking_data'] = bool(xls_sheet.cell_value(0, 14))
    common_data['has_audio_data'] = bool(xls_sheet.cell_value(0, 16))
    return common_data

def fix_path(path):
    return abspath(path.replace('\\', sep).replace('/', sep))

def import_row(investigator, xls_sheet, common_data, row, available_cameras, db_session):
    """
    Import a row of experiment data
    """
    base_dir = common_data['base_directory']
    session = None
    experiment_date = None

    animal_nickname = int(xls_sheet.cell_value(row, 0))

    animals = db_session.query(Animal).filter(Animal.nickname == animal_nickname).all()
    if len(animals) != 1:
        print(f"Expected to find one animal with nickname {animal_nickname}, got {len(animals)}")
        if len(animals) > 0:
            for animal in animals:
                print(animal)
        assert len(animals) == 1
    animal = animals[0]

    # import videos
    video_string = xls_sheet.cell_value(row, 14)
    video_names = video_string.split(';')
    videos = []
    for video_name in video_names:
        video = VideoData()
        video.file_path = video_name.strip()

        # Get various data from video file
        video_path = fix_path(base_dir + sep + video.file_path)
        try:
            reader = seqIo_reader(video_path)
        except Exception:
            print(f"Error trying to open video file {video_path}")
            raise

        video.sample_rate = reader.header['fps']
        ts = reader.getTs(1)[0]
        reader.close()
        dt = datetime.fromtimestamp(ts)

        #if we haven't already, set the session's experiment date from this video file date
        if not experiment_date:
            experiment_date = dt.date()

        # set the video start time
        video.start_time = Timecode(video.sample_rate, dt.time().isoformat()).float
        for camera in available_cameras:
            if video.file_path.lower().find(camera.position.lower()) >= 0:
                video.camera = camera
        videos.append(video)

    # import poses, if any
    poses = []
    # if common_data['has_tracking_data'] and xls_sheet.cell_value(row, 15):
    if xls_sheet.cell_value(row, 15):
        pose_string = xls_sheet.cell_value(row, 15)
        pose_names = pose_string.split(';')
        for pose_name in pose_names:
            pose = PoseData()
            #TODO: need to match up pose file with video file (top <==> top, e.g.)
            pose.file_path = pose_name.strip()
            pose.sample_rate = videos[0].sample_rate
            pose.start_time = 0.0   # for now
            pose.format = ''        # MARS Top, MARS Front, DeepLabCut, SLEAP, Jellyfish, Cell Outlines (neuron A data)
            poses.append(pose)

        db_session.add_all(poses)
        db_session.commit()

    # import neural (calcium imaging) data
    neural_string = xls_sheet.cell_value(row, 4)
    neural_names = neural_string.split(';')
    neurals = []
    for neural_name in neural_names:
        neural = NeuralData()
        neural.file_path = neural_name.strip()
        neural.sample_rate = xls_sheet.cell_value(row, 7) if xls_sheet.cell_value(row, 7) else common_data['neural_framerate']
        offset = xls_sheet.cell_value(row, 14)
        neural.format = 'CNMFE' # by default
        neural.start_frame = int(xls_sheet.cell_value(row, 5))
        neural.stop_frame = int(xls_sheet.cell_value(row, 6))

        """ need to do this properly for .mat files
        # Get  various data from neural file
        reader = seqIo_reader(neural.file_path)
        ts = reader.getTs(neural.start_frame)
        reader.close()
        dt = datetime.fromtimestamp(ts)

        # set the neural start time for the start frame
        # neural.start_time = Timecode(video.sample_rate, dt.time.isoformat())
        """
        neural.start_time = videos[0].start_time # for now

        neurals.append(neural)

    # import annotation data
    annotation_string = xls_sheet.cell_value(row, 9)
    annotation_names = annotation_string.split(';')
    annotations = []
    for annotation_name in annotation_names:
        annotation = Annotations()
        annotation.file_path = annotation_name.strip()
        annotation.sample_rate = float(xls_sheet.cell_value(row, 12)) if xls_sheet.cell(row, 12).ctype == xlrd.XL_CELL_NUMBER else videos[0].sample_rate
        annotation.start_time = videos[0].start_time + float(xls_sheet.cell_value(row, 13))  # for now
        annotation.start_frame = int(xls_sheet.cell_value(row, 10)) if xls_sheet.cell(row, 10).ctype == xlrd.XL_CELL_NUMBER else 0
        annotation.stop_frame = int(xls_sheet.cell_value(row, 11)) if xls_sheet.cell(row, 11).ctype == xlrd.XL_CELL_NUMBER else 0
        annotation.format = 'MAT'
        annotations.append(annotation)

    # import audio data, if any
    audios = []
    # if common_data['has_audio_data'] and xls_sheet.cell_value(row, 16):
    if xls_sheet.cell_value(row, 16):
        audio_string = xls_sheet.cell_value(row, 16)
        audio_names = audio_string.split(';')
        for audio_name in audio_names:
            audio = AudioData()
            audio.file_path = audio_name.strip()
            audio.sample_rate = videos[0].sample_rate #TODO: is this right?
            audio.processed_audio_path = ''
            # audio.annotations_id = 0
            audios.append(audio)

    if videos: db_session.add_all(videos)
    if poses: db_session.add_all(poses)
    if neurals: db_session.add_all(neurals)
    if annotations: db_session.add_all(annotations)
    if audios: db_session.add_all(audios)

    trial = Trial()
    trial.trial_num = int(xls_sheet.cell_value(row, 2))
    trial.stimulus = xls_sheet.cell_value(row, 3)
    trial.video_data = videos
    trial.audio_data = audios
    trial.neural_data = neurals
    trial.pose_data = poses
    trial.annotations = annotations
    trial.other_data = []

    # get the appropriate existing session, or create a new one
    animal_id = animal.id
    investigator_id = investigator.id
    session_num = int(xls_sheet.cell_value(row, 1))
    query = db_session.query(Session).filter(Session.investigator_id == investigator_id)
    query = query.filter(Session.animal_id == animal_id)
    query = query.filter(Session.session_num == session_num)
    query = query.filter(Session.experiment_date == experiment_date)
    sessions = query.all()

    if len(sessions) > 1:
        print("DB error: more than one database entry with"
            " the same investigator, animal, session number and date")
        return
    elif len(sessions) == 1:
        session = sessions[0]
    elif len(sessions) == 0:
        # Build a new session
        session = Session()
        session.investigator_id = investigator_id
        session.animal_id = animal_id
        session.session_num = session_num
        session.base_directory = base_dir
        session.experiment_date = experiment_date
        db_session.add(session)

    session.trials.append(trial)
    db_session.add(trial)
    db_session.commit()

def import_bento_xls_file(file_path, db_session, investigator):
    abs_path = abspath(file_path)
    base_dir = dirname(abs_path)

    xls = xlrd.open_workbook(abs_path)
    sheet = xls.sheets()[0]

    common_data = import_common_info(sheet, base_dir)

    available_cameras = db_session.query(Camera).all()

    for row in range(2, sheet.nrows):
        import_row(investigator, sheet, common_data, row, available_cameras, db_session)

def do_import(investigator_name, rel_path):
    Session = new_session()
    sess = Session()
    investigators = sess.query(Investigator).filter(Investigator.user_name == investigator_name).all()
    assert len(investigators) == 1
    investigator = investigators[0]

    import_bento_xls_file(rel_path, sess, investigator)

