***********
Development
***********

Editable Installation from Source
=================================

API Documentation
=================

.. automodule:: betrack.cli

Commands
--------

command
^^^^^^^

.. automodule:: betrack.commands.command

    .. autoclass:: betrack.commands.command.BetrackCommand

        .. automethod:: betrack.commands.command.BetrackCommand.__init__

        .. automethod:: betrack.commands.command.BetrackCommand.run
			

annotatevideo
^^^^^^^^^^^^^

.. automodule:: betrack.commands.annotatevideo

    .. autoclass:: betrack.commands.annotatevideo.AnnotateVideo

        .. automethod:: betrack.commands.annotatevideo.AnnotateVideo.__init__

        .. automethod:: betrack.commands.annotatevideo.AnnotateVideo.configure_annotator

        .. automethod:: betrack.commands.annotatevideo.AnnotateVideo.draw_particles

        .. automethod:: betrack.commands.annotatevideo.AnnotateVideo.draw_region

        .. automethod:: betrack.commands.annotatevideo.AnnotateVideo.draw_frame_number
			
        .. automethod:: betrack.commands.annotatevideo.AnnotateVideo.annotator
			
        .. automethod:: betrack.commands.annotatevideo.AnnotateVideo.run
			

trackparticles
^^^^^^^^^^^^^^

.. automodule:: betrack.commands.trackparticles

    .. autoclass:: betrack.commands.trackparticles.TrackParticles

        .. automethod:: betrack.commands.trackparticles.TrackParticles.__init__

        .. automethod:: betrack.commands.trackparticles.TrackParticles.configure_tracker
			
        .. automethod:: betrack.commands.trackparticles.TrackParticles.locate_features
			
        .. automethod:: betrack.commands.trackparticles.TrackParticles.link_trajectories
			
        .. automethod:: betrack.commands.trackparticles.TrackParticles.filter_trajectories
			
        .. automethod:: betrack.commands.trackparticles.TrackParticles.export_video
			
        .. automethod:: betrack.commands.trackparticles.TrackParticles.run
			
			
Utils
-----

frames
^^^^^^

.. automodule:: betrack.utils.frames
		
    .. automethod:: betrack.utils.frames.as_gray
		
    .. automethod:: betrack.utils.frames.crop
		
    .. automethod:: betrack.utils.frames.flip
		
    .. automethod:: betrack.utils.frames.invert_colors
		
    .. automethod:: betrack.utils.frames.reverse_colors
		   		   

job
^^^

.. automodule:: betrack.utils.job

    .. autoclass:: betrack.utils.job.Job

        .. automethod:: betrack.utils.job.Job.__init__

        .. automethod:: betrack.utils.job.Job.str

        .. automethod:: betrack.utils.job.Job.load_frames

        .. automethod:: betrack.utils.job.Job.release_memory

        .. automethod:: betrack.utils.job.Job.export_trajectories

        .. automethod:: betrack.utils.job.Job.valid_margins			
			
        .. automethod:: betrack.utils.job.Job.preprocess_video

    .. automethod:: betrack.utils.job.configure_jobs			
			
			
message
^^^^^^^

.. automodule:: betrack.utils.message

    .. autoclass:: betrack.utils.message.Message
		   
        .. automethod:: betrack.utils.message.Message.disable

    .. automethod:: betrack.utils.message.mprint
		    
    .. automethod:: betrack.utils.message.wprint
		    
    .. automethod:: betrack.utils.message.eprint			


parser
^^^^^^

.. automodule:: betrack.utils.parser

    .. automethod:: betrack.utils.parser.open_configuration
		    
    .. automethod:: betrack.utils.parser.parse_file
		    
    .. automethod:: betrack.utils.parser.parse_directory
		    
    .. automethod:: betrack.utils.parser.parse_int
		    
    .. automethod:: betrack.utils.parser.parse_float
		    
    .. automethod:: betrack.utils.parser.parse_int_or_float
		    
    .. automethod:: betrack.utils.parser.parse_bool
		    
    .. automethod:: betrack.utils.parser.parse_str

		    
